testing_set = ["Nike Vaporfly Nexts",
"Nike Vapor Fly",
"Nike Next %",
"Nike Vaporfly Next%",
"Nike Next %",
"Nike Pink NEXT%",
"Nike Zoom Vaporfly Next% - Lime",
"Nike Vaporfly Next % (Green Fluo) Nov 19",
"Nike Vapourfly Next%",
"Nike VF next, par 1. 29/7-19",
"Nike Zoom Next",
"Nike ZoomX Vaporfly Next%",
"Nike Vaporfly Air Kipchoge",
"Nike Vaporfly",
"Nike Zoom Fly 4%",
"Nike vaporfly next",
"Nike Vaporfly Next% Slimer",
"Nike Next%",
"Nike VF4% Next",
"Nike Next %",
"Nike Vaporfly Flyknit 4%",
"Nike 4%",
"Nike Nike Vapofly Next%",
"Nike Vaporfly %",
"Nike 4% Vaporfly",
"Nike Vaporfly 4% (Red)",
"Nike vaporfly next",
"Nike Vaporfly 4% Flyknit",
"Nike ZoomX Vaporfly",
"Nike ZoomX Vaporfly Next%",
"Nike zoom vaporfly 4%",
'Nike ZoomX Vaporfly Next% Gn/Bk',
"Nike ZoomX Vaporfly",
"Nike Vapor Fly Next",
"Nike VaporFly 4%",
"Nike ZoomX Vaporfly Next%",
"Nike Vaporfly 4% Blue",
"Nike Vaporfly Next% Pink (10.0)",
"Nike Zoom X Vaporfly Next%",
"Nike Vaporfly 4% Flyknit Bright Crimson Sapphire",
"Nike Next % pink",
'Nike Vaporfly Next Oct 2019',
"Nike %next",
"Nike Vaporfly Next% Green",
"Nike Vaporfly Next (#2)",
"Nike ZoomX Vaporfly NEXT% - Pink",
"Nike Vaporfly Next% Green",
"Nike Vaporfly Next% - Neon Green",
"Nike Nike ZoomX Vaporfly NEXT% (10)",
"Nike ZoomX Vaporfly Next%"]

checks = ["%", "vf", "fly", "next", "vapor", "vapour"]

final_lst = []

for shoe in testing_set:
	for check in checks:
		if check in shoe:
			final_lst.append(shoe)

final_lst = set(final_lst)

print("Success rate is: ", len(final_lst)/len(testing_set))