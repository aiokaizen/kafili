#
# class Page:
#
#     def __init__(self, title, url='', parents=None):
#         self.title = title
#         self.url = url
#         self.parents = []
#         self.set_parents(parents)
#
#     def set_parents(self, parents):
#         if parents:  # parents is not None and len(parents) > 0
#             if type(parents) == list().__class__ and (len(parents) > 0 and type(parents[0]) == self.__class__):
#                 self.parents = parents
#             else:
#                 raise Exception('Parent has to be a Page instance, not a ' + str(parents[0].__class__) + ' instance.')
#
#
# def get_page_parents_from_path(path):
#     uri = ''
#     parents = []
#     for elt in path.split('/')[1:-2]:
#         uri += '/' + elt
#         parents.append(Page(elt, uri))
#     return parents


class Page:

    def __init__(self, title, label='', url='', parent=None):
        self.title = title
        self.label = ''
        self.set_label(label)
        self.url = url
        self.parent = None
        self.set_parent(parent)

    def set_label(self, label):
        self.label = label if label else self.title

    def set_parent(self, parent):
        if parent:  # parents is not None and len(parents) > 0
            if type(parent == self.__class__):
                self.parent = parent
            else:
                raise Exception('Parent has to be a Page instance, not a ' + str(parent.__class__) + ' instance.')


def get_page_parents(page, depth=0):
    parents = []
    index = 0
    while page.parent is not None:
        parents.append(page.parent)
        page = page.parent
        if depth != 0:
            if index == depth:
                break
            index += 1
    parents.reverse()
    return parents
