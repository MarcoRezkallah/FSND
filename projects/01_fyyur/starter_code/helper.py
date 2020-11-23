import json

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

    def map_venue(venue):
        genres = json.loads(venue.genres)
        out = {
            "id": venue.id,
            "name": venue.name,
            "genres": genres,
            "address": venue.address,
            "city": venue.city,
            "state": venue.state,
            "phone": venue.phone,
            "website": venue.website,
            "facebook_link": venue.facebook_link,
            "seeking_talent": venue.seeking_talent or False,
            "image_link": venue.image_link,
            "past_shows": [{
                "artist_id": 5,
                "artist_name": "Matt Quevedo",
                "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
                "start_time": "2019-06-15T23:00:00.000Z"
            }],
            "upcoming_shows": [{
                "artist_id": 6,
                "artist_name": "The Wild Sax Band",
                "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
                "start_time": "2035-04-01T20:00:00.000Z"
            }],
            "past_shows_count": 1,
            "upcoming_shows_count": 1,
        }
        return out

    def map_artist(artist):
        genres = json.loads(artist.genres)
        out = {
            "id": artist.id,
            "name": artist.name,
            "genres": genres,
            "city": artist.city,
            "state": artist.state,
            "phone": artist.phone,
            "website": artist.website,
            "facebook_link": artist.facebook_link,
            "seeking_venue": artist.seeking_venue or False,
            "image_link": artist.image_link,
            "past_shows": [{
                "artist_id": 5,
                "artist_name": "Matt Quevedo",
                "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
                "start_time": "2019-06-15T23:00:00.000Z"
            }],
            "upcoming_shows": [{
                "artist_id": 6,
                "artist_name": "The Wild Sax Band",
                "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
                "start_time": "2035-04-01T20:00:00.000Z"
            }],
            "past_shows_count": 1,
            "upcoming_shows_count": 1,
        }
        return out

    def map_shows(showList):
        data = []
        for s in showList:
            data.append({
                "venue_id": s.venue.id,
                "venue_name": s.venue.name,
                "artist_id": s.artist.id,
                "artist_name": s.artist.name,
                "artist_image_link": s.artist.image_link,
                "start_time": s.start_time.isoformat()
            })
        return data
