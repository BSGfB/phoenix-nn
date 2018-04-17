SELECT
  i.original_url as url,
  d.label_display_name as name,
  ab.x_min as x1,
  ab.x_max as x2,
  ab.y_min as y1,
  ab.y_max as y2
FROM [bigquery-public-data:open_images.images] AS i
LEFT JOIN [bigquery-public-data:open_images.labels] AS l ON i.image_id = l.image_id
LEFT JOIN [bigquery-public-data:open_images.dict] AS d ON d.label_name = l.label_name
LEFT JOIN [bigquery-public-data:open_images.annotations_bbox] AS ab ON ab.image_id = i.image_id
WHERE
  UPPER(d.label_display_name) = UPPER('Iphone') OR
  UPPER(d.label_display_name) = UPPER('Smartphone') AND
  l.confidence > 0.9;