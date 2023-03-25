class Database(dict):
    def add_object(self, obj):
        self[obj.object_id] = obj

    def get_object_by_id(self, object_id):
        return self.get(object_id, None)

    def get_objects_by_object_type(self, object_type):
        return [obj for obj in self.values() if obj.get_object_type() == object_type]

db = Database()