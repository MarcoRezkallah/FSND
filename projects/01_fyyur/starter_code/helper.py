

class helper:
    def map_venues(venueList):
        output = {}
        data = []
        for vn in venueList:
            v = {}
            v['id'] = vn.id
            v['name'] = vn.name
            v['num_upcoming_shows'] = 0  # TODO: handle calculations

            try:
                output[vn.state][vn.city].append(v)
            except:
                try:
                    output[vn.state][vn.city] = []
                except:
                    output[vn.state] = {}
                    output[vn.state][vn.city] = []
                output[vn.state][vn.city] = []
                output[vn.state][vn.city].append(v)

        for state, value in output.items():
            for city, venues in value.items():
                obj = {}
                obj['city'] = city
                obj['state'] = state
                obj['venues'] = venues
                data.append(obj)

        return data
