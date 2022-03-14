import math

class Node:
    yx = ()
    g = 0
    h = 0
    f = 0
    tip = ""
    came_from = None

    def __init__(self, y, x, g, h, f, tip):
        self.yx = (y, x)
        self.g = g
        self.h = h
        self.f = f
        self.d = g
        self.tip = tip
        self.came_from = None


class AStar:
    graf = []
    start = ()
    cilj = ()
    zakladi = []
    nodes = []
    open_list = []
    closed_list = []
    path = []
    total_path = []
    iskanje_zakladov = True
    pogoj = False
    stevilo_odprtih = 0
    odprta = set()

    def __init__(self, datoteka):
        dato = self.read_file(datoteka)
        self.graf = dato[0]
        self.nodes = dato[1]
        self.cilj = dato[2]
        self.start = dato[3]
        self.zakladi = dato[4]
        self.path = []
        self.total_path = []
        self.iskanje_zakladov = True
        self.pogoj = False
        self.stevilo_odprtih = 0
        self.odprta = set()

    def hofn(self, node, cilj):
        x = 0
        y = 0
        if node.yx[1] < cilj.yx[1]:
            for ix in range(node.yx[1] + 1, cilj.yx[1] + 1):
                x += self.graf[node.yx[0]][ix]

        if node.yx[1] > cilj.yx[1]:
            for ix in range(node.yx[1] - 1, cilj.yx[1] - 1, -1):
                x += self.graf[node.yx[0]][ix]

        if node.yx[1] < cilj.yx[1]:
            for iy in range(node.yx[0] + 1, cilj.yx[0] + 1):
                y += self.graf[iy][node.yx[1]]

        if node.yx[1] < cilj.yx[1]:
            for iy in range(node.yx[0] + 1, cilj.yx[0] + 1, -1):
                y += self.graf[iy][node.yx[1]]

        return abs(math.floor(math.sqrt(x ** 2) + (y ** 2)))

    def hofn_for_zakladi(self, node):
        targets = []
        for i in self.zakladi:
            targets.append((i.yx, self.hofn(node, i)))

        cheapest = targets[0]
        for target in targets:
            if target[1] < cheapest[1]:
                cheapest = target

        return cheapest


    def poisci_sosede(self, sosedi, curr_node):
        y = curr_node.yx[0]
        x = curr_node.yx[1]
        new_sosedi = []
        n_node = self.nodes[y + 1][x]
        if n_node is not None:
            new_sosedi.append(n_node)

        e_node = self.nodes[y][x + 1]
        if e_node is not None:
            new_sosedi.append(e_node)

        s_node = self.nodes[y - 1][x]
        if s_node is not None:
            new_sosedi.append(s_node)

        w_node = self.nodes[y][x - 1]
        if w_node is not None:
            new_sosedi.append(w_node)

        nw_node = self.nodes[y + 1][x - 1]
        if nw_node is not None:
            new_sosedi.append(nw_node)

        ne_node = self.nodes[y + 1][x + 1]
        if ne_node is not None:
            new_sosedi.append(ne_node)

        sw_node = self.nodes[y - 1][x - 1]
        if sw_node is not None:
            new_sosedi.append(sw_node)

        se_node = self.nodes[y - 1][x + 1]
        if se_node is not None:
            new_sosedi.append(se_node)

        for i in new_sosedi:
            if i in sosedi:
                continue
            if i not in sosedi:
                i.g += curr_node.g
        return new_sosedi

    def najdi_najmanjsi_f(self, sosedi):
        cheapest = sosedi[0].f
        ch_i = 0
        i = 0
        for sosed in sosedi:
            if sosed.f < cheapest:
                cheapest = sosed.f
                ch_i = i
            i += 1
        return ch_i

    def najdi_najmanjsi_open_f(self, open_list):
        cheapest = open_list[0].f
        ch_i = 0
        i = 0
        for node in self.open_list:
            if node.f < cheapest:
                cheapest = node.f
                ch_i = i
            i += 1
        return ch_i

    def read_file(slef, file_name):
        nodes = []
        graf = []
        zakladi = []
        cilj = ()
        start = ()
        dat = open(file_name, "r")
        rows = dat.read().splitlines()
        for row in rows:
            graf.append(row.split(","))

        for i in range(len(graf)):
            nodesj = []
            for j in range(0, len(graf[i])):
                x = int(graf[i][j])
                graf[i][j] = x
                if x == -4:
                    node_cilj = Node(i, j, 0, 0, 0, "cilj")
                    cilj = node_cilj
                    nodesj.append(node_cilj)
                if x == -3:
                    node_zaklad = Node(i, j, 0, 0, 0, "zaklad")
                    zakladi.append(node_zaklad)
                    nodesj.append(node_zaklad)
                if x == -2:
                    node_start = Node(i, j, 0, 0, 0, "start")
                    start = node_start
                    nodesj.append(node_start)
                if x >= 0:
                    nodesj.append(Node(i, j, x, 0, 0, "hodnik"))
                if x == -1:
                    nodesj.append(None)

            nodes.append(nodesj)

        return (graf, nodes, cilj, start, zakladi)

    def printLabirint(self, tab):
        for i in range(len(tab)):
            for j in range(len(tab[i])):
                if tab[i][j] == -1:
                    print("#", end=" ")
                if tab[i][j] == -2:
                    print("S", end=" ")
                if tab[i][j] == -3:
                    print("€", end=" ")
                if tab[i][j] == -4:
                    print("F", end=" ")
                if tab[i][j] >= 0:
                    print(" ", end=" ")
                if (j == len(tab[i]) - 1):
                    print()

    def printPot(self, tab, pot):
        for i in range(len(tab)):
            for j in range(len(tab[i])):
                terkayx = (i, j)
                if terkayx in pot and tab[i][j] > 0:
                    print(".", end=" ")
                if tab[i][j] == -1 and terkayx not in pot:
                    print("#", end=" ")
                if tab[i][j] == -2:
                    print("S", end=" ")
                if tab[i][j] == -3:
                    print("€", end=" ")
                if tab[i][j] == -4:
                    print("E", end=" ")
                if tab[i][j] >= 0 and terkayx not in pot:
                    print(" ", end=" ")
                if (j == len(tab[i]) - 1):
                    print()


    def update_f(self, sosedi):
        for sosed in sosedi:
            sosed.f += sosed.g + sosed.h
        return sosedi

    def reconstruct_path(self, current_node):
        prev_node = current_node.came_from
        if prev_node is None or current_node.tip == "start" or current_node == self.start:
            return
        else:
            self.path.append(prev_node)
            for i in range(len(self.nodes)):
                for j in range(len(self.nodes[i])):
                    node = self.nodes[i][j]
                    if node is not None:
                        if node.yx == prev_node:
                            self.reconstruct_path(node)

    def calculate_totall_cost(self, path):
        cost = 0
        for i in range(len(self.graf)):
            for j in range(len(self.graf[i])):
                if (i, j) in path:
                    cost += self.graf[i][j]
        return cost


########################################################################################################################

    def search(self):
        open_list = []
        closed_list = []
        start_node = self.start

        open_list.append(start_node)
        self.stevilo_odprtih += 1
        self.odprta.add(start_node)
        current_node = start_node
        sosedi = []
        sosedi = self.poisci_sosede(sosedi, start_node)

        while len(open_list) > 0:
            # update_f
            sosedi = self.update_f(sosedi)

            current_node = open_list[self.najdi_najmanjsi_open_f(open_list)]

            if current_node in self.zakladi:
                for i in self.zakladi:
                    if i.yx == current_node.yx:
                        self.zakladi.remove(i)
                        break
                if len(self.zakladi) == 0:
                    self.iskanje_zakladov = False

                self.path.append(current_node.yx)
                self.reconstruct_path(current_node)
                self.total_path += self.path
                self.start = current_node
                self.printPot(self.graf, self.path)
                self.path = []
                print("\n")
                self.search()

            if self.pogoj:
                return

            if current_node.tip == "cilj" and len(self.zakladi) == 0:
                self.pogoj = True
                self.path.append(current_node.yx)
                self.reconstruct_path(current_node)
                self.total_path += self.path
                self.printPot(self.graf, self.path)
                print("\n")
                self.printPot(self.graf, self.total_path)
                self.path = []
                print("Pot: ", self.total_path)
                print("Cena poti: ", self.calculate_totall_cost(self.total_path))
                print("Stevilo premikov: ", len(self.total_path))
                print("Stevilo odpiranj : ", self.stevilo_odprtih)
                print("Stevilo vozlisc, ki so bila odprta : ", len(self.odprta))
                return

            open_list.remove(current_node)
            closed_list.append(current_node)

            sosedi = self.poisci_sosede(sosedi, current_node)
            for sosed in sosedi:
                if sosed in closed_list:
                    continue
                cost = current_node.g + sosed.d
                if sosed in open_list and cost < sosed.g:
                    open_list.remove(sosed)
                if sosed in closed_list and cost < sosed.g:
                    self.closed_list.remove(sosed)
                if sosed not in open_list and sosed not in closed_list:
                    open_list.append(sosed)
                    self.stevilo_odprtih += 1
                    self.odprta.add(sosed)
                    sosed.came_from = current_node.yx
                    sosed.g = cost
                    if self.iskanje_zakladov:
                        sosed.f = cost + self.hofn_for_zakladi(sosed)[1]
                    if not self.iskanje_zakladov:
                        sosed.f = cost + self.hofn(sosed, self.cilj)

        print("failed to find path")


iskanje = AStar("D:/FAKS/2letnik/UI/Sem2/labyrinth_7.txt")
iskanje.printLabirint(iskanje.graf)
print("\n")
iskanje.search()



