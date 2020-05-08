# this doesn't work because you can't have inputs in the outputs, you'd have to
# put them in state.
# the way you can make this work is by having only one input and having this
# input also be the context that triggered the callbacks, but this isn't written yet

import dash

class DashCallbackRouter:
    def __init__(self):
        self.input_id_strs=set()
        self.output_id_strs=set()
        self.state_id_strs=set()
        self.contexts=dict()
        self.input_list=None
        self.output_list=None
        self.state_list=None
        self.out_idcs_in_input_list=None
    def add_cb(self,
               output_id_strs,
               input_id_strs, #e.g., ['id.field',...]
               state_id_strs,
               cbcontext,
               cb):
        for iid in input_id_strs:
            self.input_id_strs.add(iid)
        for oid in output_id_strs:
            # also added to input because we just use the old value of the
            # output if the value is unchanged
            self.input_id_strs.add(oid)
            self.output_id_strs.add(oid)
        for sid in state_id_strs:
            self.state_id_strs.add(sid)
        # store the callback and its context
        self.contexts[cbcontext] = {
            'input_id_strs': input_id_strs,
            'output_id_strs': output_id_strs,
            'state_id_strs': state_id_strs,
            'cb': cb
        }

def register_cbs_with_app(cb_router,app):
    """ registers the callbacks with an app """
    cb_router.input_list=list(cb_router.input_id_strs)
    cb_router.output_list=list(cb_router.output_id_strs)
    cb_router.state_list=list(cb_router.state_id_strs)
    cb_router.out_idcs_in_input_list=[
        cb_router.input_list.index(i) for i in cb_router.input_list
    ]
    print([o for o in cb_router.output_list])
    print([o for o in cb_router.input_list])
    print([o for o in cb_router.state_list])
    @app.callback(
        [dash.dependencies.Output(*o.split('.')) for o in cb_router.output_list],
        [dash.dependencies.Input(*o.split('.')) for o in cb_router.input_list],
        [dash.dependencies.State(*o.split('.')) for o in cb_router.state_list]
    )
    def app_callback(*args):
        all_inputs=args[:len(cb_router.input_list)],
        all_states=args[len(cb_router.input_list):]
        all_outputs=[all_inputs[i] for i in cb_router.out_idcs_in_input_list]
        cbcontext=[p['prop_id'] for p in dash.callback_context.triggered][0]
        inputs=[
            all_inputs[cb_router.input_list.index(j)]
                    for j in cb_router.contexts[cbcontext].input_id_strs
        ]
        states=[
            all_states[cb_router.state_list.index(j)]
                    for j in cb_router.contexts[cbcontext].state_id_strs
        ]
        # now call the function
        outputs=cb_router.contexts[cbcontext].cb(inputs,states,cbcontext)
        output_idcs=[
            cb_router.output_list.index(j)
                    for j in cb_router.contexts[cbcontext].output_id_strs
        ]
        for i,o in zip(output_idcs,outputs):
            all_outputs[i]=o
        return tuple(all_outputs)
    return app_callback
