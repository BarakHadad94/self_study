names = ["barak", "sHaroN", "Eyal", 23]
print("Hello " + names[0].title() + "!")
print("Hello " + names[1].title() + "!")
print("Hello " + names[2].title() + "!")
print("Hello " + str(names[3]) + "!\n\n")

magicians = ['barak', 'yael', 'aba']
for magician in magicians:
	print(magician)

cubes = [value**3 for value in range(1,10)]
print(cubes)

new_cubes = cubes
dif_cubes = cubes[:]

cubes.append(33)
new_cubes.append(22)
dif_cubes.append(11)

print(cubes)
print(new_cubes)
print(dif_cubes)

dictionary = {'name' : 'barak', 'last' : 'hadad'}
for name, last in dictionary.items():
	print(name.title() + " " + last)

milon = {'bhadad' : {'first' : 'Barak', 'last' : 'Hadad'}, 'shadad' : {'first' : 'Sharon', 'last' : 'Hadad'}}
for obj, det in milon.items():
	print(obj + "\n" + det['first'] + " " + det['last'])