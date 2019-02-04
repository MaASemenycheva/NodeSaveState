class Node():

    def __init__(self, node_id, next_node, answer):
        """
        node_id - id текущей ноды
        next_node - id следующей ноды
        answer - string ответ текущей ноды
        """
        self.node_id = node_id
        self.next_node = next_node
        self.answer = answer

    def get_answer(self):
        return self.answer

    def to_dict(self):
        return {'id': self.node_id,
                'next_node': self.next_node,
                'answer': self.answer
                }


#ключ - это твой chat_id
#значение - это id ноды
class SavedState(object):
    def __init__(self):
        self._dictionary = dict()

    def set_state(self, chat_id, node_id):
        self._dictionary[chat_id] = node_id

    def take_state(self, chat_id):
        if chat_id in self._dictionary:
            return self._dictionary[chat_id]
        else:
            return None

    def delete_record_from_dictionary(self, chat_id):
        if chat_id in self._dictionary:
            del self._dictionary[chat_id]


class SimplestNodeBot():
    savedstate = SavedState()

    # А теперь представь, что ключ - это твой chat_id, а значение - это id ноды
    def __init__(self, nodes):
        """
        nodes - list of Node objects
        """
        self.nodes = dict()
        for i in nodes:
            node_dict = i.to_dict()
            self.nodes[node_dict['id']] = {'next_node': node_dict['next_node'],
                                           'answer': node_dict['answer']}

    def get_answer_for_node(self, node_id):
        return self.nodes[node_id]['answer']

    #     def find_answer(self, chat_id):
    #         state = self.savedstate.take_state(chat_id)

    #         if state==None:
    #             node = self.nodes[0]# 0#self.nodes[0]
    #             next_node = self.nodes[node['next_node']]
    #             self.savedstate.set_state(chat_id, next_node)
    #             return node['answer']#self.get_answer_for_node(node)

    #         else:
    #             node = state
    #             if node['next_node'] is None:
    #                 self.savedstate.set_state(chat_id, self.nodes[0])
    #             else:
    #                 self.savedstate.set_state(chat_id, self.nodes[node['next_node']])

    #             return node['answer']

    def find_answer(self, chat_id):
        # запрос состояния
        state = self.savedstate.take_state(chat_id)
        print("----------")
        print(state)
        if state == None:
            node_id = 0
            # меняем состояние
            next_node_id = self.nodes[node_id]['next_node']
            self.savedstate.set_state(chat_id, next_node_id)
            # берём ответ этого node_bot-а
            return self.get_answer_for_node(node_id)

        else:
            # savedstate.set_state(chat_id, node_id)
            if self.nodes[state]['next_node'] is None:
                self.savedstate.set_state(chat_id, 0)
            else:
                self.savedstate.set_state(chat_id, self.nodes[state]['next_node'])
            return self.get_answer_for_node(state)
