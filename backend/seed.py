from app import create_app, db
from app.models.art import Art

app = create_app()

with app.app_context():
    print("📦 Dropping old tables...")
    db.drop_all()

    print("📐 Creating tables...")
    db.create_all()

    print("🎨 Seeding data...")
    artworks = [
        Art(name="Ocean Breeze", description="A calming ocean painting", category_id=1, tag_id=101, price=250.0),
        Art(name="Mountain Sunrise", description="Bright morning over mountains", category_id=2, tag_id=102, price=310.5),
        Art(name="City Lights", description="Night cityscape in oil", category_id=3, tag_id=103, price=420.75),
    ]

    db.session.add_all(artworks)
    db.session.commit()
    print("✅ Sample data inserted!")
