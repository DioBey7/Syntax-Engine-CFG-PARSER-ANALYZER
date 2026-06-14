class Interpreter:
    def __init__(self):
        self.environment = {}

    def evaluate(self, node):
        if isinstance(node, str):
            if node.replace('.', '', 1).isdigit():
                return float(node) if '.' in node else int(node)
            return node
        
        if isinstance(node, dict):
            
            if "spawn" in node.values() and "<npc>" in node:
                npc = self.evaluate(node["<npc>"])
                zone = self.evaluate(node["<zone>"])
                return f"SYSTEM: [{npc.upper()}] named entity loaded at the [{zone.upper()}] region."

            if "set" in node.values() and "=" in node.values() and "<attribute>" in node:
                attribute = self.evaluate(node["<attribute>"])
                value = self.evaluate(node["<value>"])
                self.environment[attribute] = value 
                return f"ENGINE: NPC '{attribute}' variable assigned {value} as its value. (Memory Saved)"

            last_result = None
            for key, value in node.items():
                res = self.evaluate(value)
                if res is not None:
                    last_result = res
            return last_result
            
        return None