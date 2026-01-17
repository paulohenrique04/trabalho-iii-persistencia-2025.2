classDiagram
    class Movie {
        +ObjectId _id
        +String title
        +ObjectId[] actor_ids
        +ObjectId[] genre_ids
    }
    
    class Actor {
        +ObjectId _id
        +String name
    }
    
    class Review {
        +ObjectId _id
        +ObjectId movie_id
        +ObjectId user_id
        +Float rating
    }
    
    Movie --> "*" Actor : references via actor_ids
    Review --> "1" Movie : references via movie_id
    Review --> "1" User : references via user_id