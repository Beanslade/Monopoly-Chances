class Player:
    def __init__(self, player_id, position, double_count, jail_count):
        self._player_id = player_id
        self._position = position
        self._double_count = double_count
        self._jail_count = jail_count

    def get_id(self):
        return self._player_id

    def get_position(self):
        return self._position

    def update_position(self, new_position):
        if new_position > 39:
            self._position = new_position - 40
        elif new_position < 0:
            self._position = new_position + 40
        else:
            self._position = new_position

    def update_position_jail(self):
        self._position = 40

    def get_double_count(self):
        return self._double_count

    def inc_double_count(self):
        self._double_count += 1

    def reset_double_count(self):
        self._double_count = 0

    def get_jail_count(self):
        return self._jail_count

    def inc_jail_count(self):
        self._jail_count += 1

    def reset_jail_count(self):
        self._jail_count = 0
