CREATE VIEW if NOT EXISTS PictureWithLikesCount AS
SELECT p.id, p.picture, p.description, p.key, p.lastViewTime, p.viewCounter, p.author_id, p.uploadTime,
       CASE WHEN l.like_count IS NULL THEN 0 ELSE l.like_count END as "like_count",
       CASE WHEN d.dislike_count IS NULL THEN 0 ELSE d.dislike_count END as "dislike_count",
       CASE WHEN l.like_count IS NULL THEN 0 ELSE l.like_count END + CASE WHEN d.dislike_count IS NULL THEN 0 ELSE d.dislike_count END as "likes_number"
FROM Core_picture as p
              LEFT OUTER JOIN
     (
       SELECT picture_id, count() as "like_count"
       FROM Core_likes
       WHERE like=1
       GROUP by picture_id
     ) as l on p.id=l.picture_id
              left outer join
     (
       SELECT picture_id, count() as "dislike_count"
       FROM Core_likes
       WHERE like=0
       GROUP by picture_id
     ) as d on p.id=d.picture_id;