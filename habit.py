from datetime import date

class Habit:

    def __init__(self, username, category, name, count, start_date, last_modified_date, max_quit_count):
        self.username = username
        self.category = category
        self.name = name
        self.count = count
        self.start_date = start_date
        self.last_modified_date = last_modified_date
        self.max_quit_count = max_quit_count

    def __repr__(self):
        return "Habit('{}','{}','{}','{}','{}','{}','{}', {})".format(self.username, self.category, self.name, self.count, self.start_date, self.last_modified_date, self.max_quit_count)
        