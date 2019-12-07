import re

class NodeActions(object):
    def __str__(self):
        text = []
        for aindex, aname, aorder, show_fn, run_fn, html_generator in self:
            text.append("%s: %s, %s, %s, %s" %(aindex, aname, show_fn, run_fn, html_generator))
        return '\n'.join(text)

    def __iter__(self):
        for aindex, (aname, aorder, show_fn, run_fn, html_generator) in self.actions.items():
            yield (aindex, aname, aorder, show_fn, run_fn, html_generator)

    def __init__(self):
        self.actions = {}

    def clear_default_actions(self):
        self.actions = {}

    def add_action(self, action_strid, action_name, display_order, show_fn, run_fn, html_generator):
        #aindex = "act_"+id_generator()
        aindex = re.sub(r"\s+", '_', action_strid)
        self.actions[aindex] = [action_name, display_order, show_fn, run_fn, html_generator]
