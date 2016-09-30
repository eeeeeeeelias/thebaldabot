import shelve

token = "239639665:AAEJepjZ_Tb7ppPHdluw0pSx8UgvGyMD_-c"

now_word = {}
user_ids = shelve.open("ids")
user_vocabs = {}
for key in user_ids:
	d = shelve.open(key)
	user_vocabs[int(key)] = d
print("<---------------------->")
print([key for key in user_ids])
print("<---------------------->")
waiting_for_answer = False
game_is_now = False
debugging = False