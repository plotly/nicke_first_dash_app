# this doesn't work because you can't have inputs in the outputs, you'd have to
# put them in state.
# the way you can make this work is by having only one input and having this
# input also be the context that triggered the callbacks, but this isn't written yet

import dash
import pdb

class DashCallbackRouter:
    def __init__(self):
        self.input_id_strs=set()
        self.output_id_strs=set()
        self.state_id_strs=set()
        self.contexts=dict()
        self.input_list=None
        self.output_list=None
        self.state_list=None
        self.out_idcs_in_state_list=None
    def add_cb(self,
               output_id_strs,
               input_id_str, #e.g., ['id.field',...]
               state_id_strs,
               cb):
        self.input_id_strs.add(input_id_str)
        for oid in output_id_strs:
            # added to state because we just use the old value of the
            # output if the value is unchanged
            self.state_id_strs.add(oid)
            self.output_id_strs.add(oid)
        for sid in state_id_strs:
            self.state_id_strs.add(sid)
        # store the callback and its context
        self.contexts[input_id_str] = {
            'output_id_strs': output_id_strs,
            'state_id_strs': state_id_strs,
            'cb': cb
        }

def register_cbs_with_app(cb_router,app):
    """ registers the callbacks with an app """
    cb_router.input_list=list(cb_router.input_id_strs)
    cb_router.output_list=list(cb_router.output_id_strs)
    cb_router.state_list=list(cb_router.state_id_strs)
    cb_router.out_idcs_in_state_list=[
        cb_router.state_list.index(i) for i in cb_router.output_list
    ]
    @app.callback(
        [dash.dependencies.Output(*o.split('.')) for o in cb_router.output_list],
        [dash.dependencies.Input(*o.split('.')) for o in cb_router.input_list],
        [dash.dependencies.State(*o.split('.')) for o in cb_router.state_list]
    )
    def app_callback(*args):
        print("args:",args)
        print("input_list:",cb_router.input_list)
        all_inputs=args[:len(cb_router.input_list)]
        print("all_inputs",all_inputs)
        all_states=args[len(cb_router.input_list):]
        all_outputs=[all_states[i] for i in cb_router.out_idcs_in_state_list]
        cbcontext=[p['prop_id'] for p in dash.callback_context.triggered][0]
        print(cbcontext)
        if cbcontext not in cb_router.input_list:
            return dash.no_update
        input=all_inputs[cb_router.input_list.index(cbcontext)]
        states=[
            all_states[cb_router.state_list.index(j)]
                    for j in cb_router.contexts[cbcontext]['state_id_strs']
        ]
        # now call the function
        outputs=cb_router.contexts[cbcontext]['cb'](input,states)
        output_idcs=[
            cb_router.output_list.index(j)
                    for j in cb_router.contexts[cbcontext]['output_id_strs']
        ]
        for i,o in zip(output_idcs,outputs):
            all_outputs[i]=o
        return tuple(all_outputs)
    return app_callback
