from app import app, db
from models import Route, BoardingPoint
from datetime import time


def import_cet_routes():
    with app.app_context():
        # Clear existing data
        BoardingPoint.query.delete()
        Route.query.delete()

        # Create routes
        routes_data = [
            {"number": "S1", "name": "Avadi"},
            {"number": "S2", "name": "Ayanavaram"},
            {"number": "S3", "name": "Koyambedu"},
            {"number": "S4", "name": "Mylapore"},
            {"number": "S5", "name": "Nandambakkam"},
            {"number": "S6", "name": "Thiruvottriyur"},
            {"number": "S7", "name": "Velachery"},
            {"number": "S7A", "name": "Pallikaranai"},
            {"number": "S8", "name": "Mount Subway"},
            {"number": "S9", "name": "Padappai"},
            {"number": "S10", "name": "Chengalpat"},
            {"number": "S11", "name": "Chrompet"},
            {"number": "S12", "name": "Senthil Nagar"}
        ]

        # Create boarding points dictionary
        boarding_points_data = {
            "S1": [
                (1, "Avadi", time(6, 20)),
                (2, "Thirumullaivoyal", time(6, 27)),
                (3, "Ambattur OT", time(6, 35)),
                (4, "Decathlon Service road", time(6, 45)),
                (5, "Porur Toll Gate", time(6, 55))
            ],
            "S2": [
                (1, "Kellys", time(6, 5)),
                (2, "Mental Hospital (Keezhpak)", time(6, 10)),
                (3, "Ayanavaram Singnal", time(6, 12)),
                (4, "Noor Hotel", time(6, 15)),
                (5, "Joint Office", time(6, 20)),
                (6, "Pollice Quatras", time(6, 22)),
                (7, "ICF", time(6, 25)),
                (8, "Nathamuni", time(6, 30)),
                (9, "Anna Nagar West Depot", time(6, 35)),
                (10, "Rohini Theatre", time(6, 40)),
                (11, "Madhuravoyal Erikarai", time(6, 50))
            ],
            "S3": [
                (1, "Koyambedu", time(6, 15)),
                (2, "MMDA", time(6, 20)),
                (3, "Vadapalani", time(6, 25)),
                (4, "Ashok Pillar", time(6, 29)),
                (5, "Kasi Theatre", time(6, 32)),
                (6, "Ekkattuthangal", time(6, 35)),
                (7, "Pallavaram", time(6, 50)),
                (8, "MIT Chrompet", time(7, 0))
            ],
            # Add other routes similarly
        }

        # Insert routes and boarding points
        routes = {}
        for route_data in routes_data:
            route = Route(route_number=route_data["number"], route_name=route_data["name"])
            db.session.add(route)
            db.session.flush()  # Get the ID
            routes[route_data["number"]] = route.id

            # Add boarding points if available
            if route_data["number"] in boarding_points_data:
                for point in boarding_points_data[route_data["number"]]:
                    bp = BoardingPoint(
                        stop_number=point[0],
                        location=point[1],
                        pickup_time=point[2],
                        route_id=route.id
                    )
                    db.session.add(bp)

        db.session.commit()
        print("CET bus routes imported successfully!")


if __name__ == "__main__":
    import_cet_routes()
