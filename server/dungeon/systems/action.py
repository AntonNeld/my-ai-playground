from profiling import time_profiling, memory_profiling


class ActionSystem:

    def get_actions(self, ai, percepts, actions, score, label):
        output_actions = {}
        for actor_id in ai:
            try:
                percept = percepts[actor_id]
            except KeyError:
                percept = {}

            do_time_profiling = (actor_id in label
                                 and time_profiling.started)
            do_memory_profiling = (actor_id in label
                                   and memory_profiling.started)
            if do_time_profiling:
                time_profiling.set_context(label[actor_id])
            if do_memory_profiling:
                memory_profiling.set_context(label[actor_id])

            actor_ai = ai[actor_id]
            if hasattr(actor_ai, "update_state_percept"):
                actor_ai.update_state_percept(percept)
            action = actor_ai.next_action(percept)
            if hasattr(actor_ai, "update_state_action"):
                actor_ai.update_state_action(action)

            if do_time_profiling:
                time_profiling.unset_context(label[actor_id])
            if do_memory_profiling:
                memory_profiling.unset_context(label[actor_id])

            action_type = action.action_type
            if action_type == "none":
                continue
            # Don't perform actions we're not allowed to
            if (actor_id not in actions
                    or action_type not in
                    actions[actor_id]):
                continue
            # Apply cost of action, if any
            if (actions[actor_id][action_type].cost
                    is not None
                    and actor_id in score):
                cost = actions[actor_id][action_type].cost
                score[actor_id] -= cost
            output_actions[actor_id] = action
        return output_actions
