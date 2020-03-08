testing_set = ['Nike Vaporfly Next% Pink (10.0)',
 'Nike Next % pink',
 'Nike Vaporfly Next (#2)',
 'Nike Vaporfly',
 'Nike Next %',
 'Nike Zoom Next',
 'Nike VF4% Next',
 'Nike ZoomX Vaporfly NEXT% - Pink',
 'Nike Vaporfly Next% - Neon Green',
 'Nike Vaporfly 4% Flyknit',
 'Nike Vaporfly Flyknit 4%',
 'Nike Vaporfly Nexts',
 'Nike Nike Vapofly Next%',
 'Nike VaporFly 4%',
 'Nike Vaporfly Next%',
 'Nike Vaporfly Next % (Green Fluo) Nov 19',
 'Nike Vaporfly %',
 'Nike ZoomX Vaporfly',
 'Nike Vaporfly Next Oct 2019',
 'Nike Vapor Fly Next',
 'Nike Vaporfly 4% Blue',
 'Nike Zoom Fly 4%',
 'Nike 4%',
 'Nike VF next, par 1. 29/7-19',
 'Nike Vaporfly Air Kipchoge',
 'Nike vaporfly next',
 'Nike Nike ZoomX Vaporfly NEXT% (10)',
 'Nike Pink NEXT%',
 'Nike Next%',
 'Nike 4% Vaporfly',
 'Nike Vapourfly Next%',
 'Nike zoom vaporfly 4%',
 'Nike %next',
 'Nike Vaporfly Next% Green',
 'Nike ZoomX Vaporfly Next% Gn/Bk',
 'Nike ZoomX Vaporfly Next%',
 'Nike Zoom X Vaporfly Next%',
 'Nike Vaporfly 4% Flyknit Bright Crimson Sapphire',
 'Nike Vaporfly Next% Slimer',
 'Nike Vapor Fly',
 'Nike Zoom Vaporfly Next% - Lime',
 'Nike Vaporfly 4% (Red)']

checks = ["%", "vf", "fly", "next", "vapor", "vapour"]

final_lst = []

for shoe in testing_set:
	for check in checks:
		if check in shoe.lower():
			final_lst.append(shoe) # might be more efficient to 
			# find a way to break here if there is a match

final_lst = set(final_lst)

print("Success rate is: ", len(final_lst)/len(testing_set))