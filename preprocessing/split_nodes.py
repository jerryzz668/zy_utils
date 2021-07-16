# @Description: Split nodes
# @Author     : zhangyan
# @Time       : 2020/12/9 6:10 下午
class Node:
    def __init__(self, name='', supported=True, in_nodes=None, out_nodes=None):
        self.name = name
        self.supported = supported
        self.in_nodes = []
        self.out_nodes = []

    def draw(self, result=''):
        for node in self.in_nodes:
            content = node.name + '->' + self.name + ',' if self.supported==node.supported else node.name.lower() + '->' + self.name + ','
            if result.find(content) == -1:
                result += content
                print(content)
                if self.supported == node.supported:
                    node.draw(result)
        for node in self.out_nodes:
            content = self.name + '->' + node.name + ',' if self.supported==node.supported else self.name + '->' + self.name.lower() + ','
            if result.find(content) == -1:
                result += content
                print(content)
                if self.supported == node.supported:
                    node.draw(result)

if __name__ == '__main__':
    # a = 'A'
    #
    # print(a.lower())
    # exit(0)
    # describe the node graph
    a = Node('A', True)
    b = Node('B', False)
    c = Node('C', True)
    d = Node('D', False)
    e = Node('E', True)
    f = Node('F', True)

    a.out_nodes.append(b)
    b.in_nodes.append(a)

    b.out_nodes.append(c)
    c.in_nodes.append(b)

    b.out_nodes.append(d)
    d.in_nodes.append(b)

    d.out_nodes.append(e)
    e.in_nodes.append(d)

    e.out_nodes.append(f)
    f.in_nodes.append(e)

    c.out_nodes.append(f)
    f.in_nodes.append(c)

    output = b.draw()