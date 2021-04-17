class Position:
    def __init__(self, pos_id, colour="white", cost=0, house_price=0, rents=None, rent_index=0):
        self.pos_id = pos_id
        self._times_visited = 0
        self._colour = colour
        self._cost = cost
        self._house_price = house_price
        if rents is None:
            self._rents = []
        else:
            self._rents = rents
        self._rent_index = rent_index

    def new_visit(self):
        self._times_visited += 1

    def get_visits(self):
        return self._times_visited

    def get_colour(self):
        return self._colour

    def is_colour(self, colour):
        return self._colour == colour

    def get_cost(self):
        return self._cost

    def get_house_price(self):
        return self._house_price

    def get_rent(self, index=None):
        if index is None:
            index = self.get_rent_index()
        return self._rents[index]

    def inc_rent_index(self):
        if self._rent_index < len(self._rents) - 1:
            self._rent_index += 1

    def dec_rent_index(self):
        if self._rent_index > 0:
            self._rent_index -= 1

    def get_rent_index(self):
        return self._rent_index

    def get_mortgage_value(self):
        return self._cost/2
