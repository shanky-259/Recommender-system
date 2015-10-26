import sys
import math
import math
files = sys.argv

ratings_list = []
item_dict = {}
movie_set = set()
curruser_movieset = set()
main_user = files[2]

f = open(files[1],'r')
for line in f.readlines():
    ratings_list.append(line.split('\t'))
    lis = line.split('\t')
    try:
        item_dict[lis[2]][lis[0]] = float(lis[1])
    except:
        item_dict[lis[2]] = {}
        item_dict[lis[2]][lis[0]] = float(lis[1])

for eachrating in ratings_list:
    if eachrating[2] not in movie_set:
        movie_set.add(eachrating[2])
    if eachrating[0] == main_user:
        curruser_movieset.add(eachrating[2])

movie_list = list(movie_set)
curruser_movielist = list(curruser_movieset)

movie_notrated_user = []

for eachmovie in movie_list:
    if eachmovie not in curruser_movielist:
        movie_notrated_user.append(eachmovie)
        
weight = {}
for eachmovie in movie_notrated_user:
    weight[eachmovie] = {}
    common_users = {}
    for eachmovie1 in curruser_movielist:
        common_users[eachmovie1] = [users for users in item_dict[eachmovie].keys() for users1 in item_dict[eachmovie1].keys() if users == users1]

    for eachmovie1 in curruser_movielist:
        avg_rating = 0
        avg_rating1 = 0
        for user in common_users[eachmovie1]:
            avg_rating1 += item_dict[eachmovie1][user]
            avg_rating += item_dict[eachmovie][user]
        try:
            avg_rating = avg_rating/len(common_users[eachmovie1])
        except:
            avg_rating = 0
        try:
            avg_rating1 = avg_rating1/len(common_users[eachmovie1])
        except:
            avg_rating1 = 0
            
        numerator = 0
        denom1 = 0
        denom2 = 0
        denom = 0
        for user in common_users[eachmovie1]:
            numerator += (item_dict[eachmovie][user] - avg_rating) * (item_dict[eachmovie1][user] - avg_rating1)
            denom1 += math.pow((item_dict[eachmovie][user] - avg_rating), 2)
            denom2 += math.pow((item_dict[eachmovie1][user] - avg_rating1), 2)
        denom = math.sqrt(denom1) * math.sqrt(denom2)
        
        try:
            weight[eachmovie][eachmovie1] = numerator/denom
        except ZeroDivisionError:
            weight[eachmovie][eachmovie1] = 0.0

prediction_dict = {}
for eachmovie in movie_notrated_user:
    sorted_weights = sorted(weight[eachmovie].items(), key=lambda x: (-x[1],x[0]))
    #print(eachmovie,sorted_weights)
    neighbor_items = sorted_weights[:int(files[3])]

    num = 0
    den = 0
    for i in range(int(files[3])):
        #print(neighbor_items[i],item_dict[neighbor_items[i][0]][main_user], weight[eachmovie][neighbor_items[i]][0])

        num += (item_dict[neighbor_items[i][0]][main_user] * weight[eachmovie][neighbor_items[i][0]])
        den += weight[eachmovie][neighbor_items[i][0]]
    try:
        prediction_dict[eachmovie] = num/den
    except:
        prediction_dict[eachmovie] = 0.0
        
for i in range(len(movie_notrated_user)):
    prediction_dict[movie_notrated_user[i]] = round(prediction_dict[movie_notrated_user[i]], 5)
        
sorted_list = sorted(prediction_dict.items(), key=lambda x: (-x[1],x[0]))
final_list = sorted_list[:int(files[4])]

for eachmovie in final_list:
    print()
    print(' '.join([eachmovie[0].rstrip(), str(prediction_dict[eachmovie[0]])]))
    
    
    
    