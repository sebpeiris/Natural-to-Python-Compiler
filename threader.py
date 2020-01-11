import AST
from AST import addToClass

'''
Module contenant l'analyseur sémantique du langage Natural.
Il permet de construire le flux d'exécution du programme (avec couture).
Avec ce flux, il permet de faire de l'analyse sémantique sur le programme.
'''

@addToClass(AST.Node)
def thread(self, lastNode):
    for c in self.children:
        lastNode = c.thread(lastNode)
    lastNode.addNext(self)
    return self

@addToClass(AST.ForNode)
def thread(self, lastNode):
    beforeCond = lastNode
    exitIterator = self.children[0].thread(lastNode)
    #exitIterator.addNext(self)
    exitCond = self.children[1].thread(exitIterator)
    exitCond.addNext(self)
    exitBody = self.children[2].thread(self)
    exitBody.addNext(beforeCond.next[-1])
    return self

@addToClass(AST.IfNode)
def thread(self, lastNode):
    beforeCond = lastNode
    condition = self.children[0].thread(lastNode)
    condition.addNext(self)

    prog1 = self.children[1].thread(self)
    prog1.addNext(self)
    prog2 = self.children[2].thread(self)
    prog2.addNext(self)
    return self

def thread(tree):
    entry = AST.EntryNode()
    tree.thread(entry)
    return entry



if __name__ == "__main__":
    from naturalParser import parse
    import sys, os
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    entry = thread(ast)

    graph = ast.makegraphicaltree()
    entry.threadTree(graph)
    
    name = os.path.splitext(sys.argv[1])[0]+'-ast-threaded.pdf'
    graph.write_pdf(name) 
    print ("wrote threaded ast to", name)    