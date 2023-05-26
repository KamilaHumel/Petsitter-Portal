def count_rating(all_ratings):
    if len(all_ratings) != 0:
        rating = sum(all_ratings) / len(all_ratings)
        return rating
    else:
        rating = 0
        return rating
