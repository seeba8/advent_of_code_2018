def add_new_recipes():
    s = sum(recipes[e] for e in elves)
    if s > 9:
        recipes.append(1)
    recipes.append(s % 10)
    return recipes


def choose_new_recipe():
    for i in range(len(elves)):
        r = recipes[elves[i]]
        elves[i] = (elves[i]+1+r) % len(recipes)


def print_recipe():
    s = ""
    for k, v in enumerate(recipes):
        if k == elves[0]:
            s += "({})".format(v)
        elif k == elves[1]:
            s += "[{}]".format(v)
        else:
            s += " {} ".format(v)
    print(s)


elves = [0, 1]
recipes = [3, 7]
# print_recipe()
while len(recipes) < 10+640441:
    add_new_recipes()
    choose_new_recipe()
    # print_recipe()
print("".join(str(x) for x in recipes[640441:640441+10]))

elves = [0, 1]
recipes = [3, 7]
search = [int(i) for i in "640441"]
ls = len(search)
found = False
i = 0
while not found:
    i += 1
    if i % 100000 == 0:
        print(len(recipes))
    add_new_recipes()
    choose_new_recipe()
    if recipes[-ls:] == search:
        print(len(recipes)-ls)
    elif recipes[-ls-1:-1] == search:
        print(len(recipes)-ls-1)
        found = True
