CREATE TABLE IF NOT EXISTS `Product` (
  `id` int PRIMARY KEY,
  `name` text,
  `sku` text,
  `image` url
);
CREATE TABLE IF NOT EXISTS `ProductSide` (
  `id` int PRIMARY KEY,
  `name` text,
  `product_id` int,
  FOREIGN KEY (product_id) REFERENCES `Product` (product_id) on delete cascade
);
CREATE TABLE IF NOT EXISTS `SideMockupSampleTestcase` (
  `id` int PRIMARY KEY,
  `testcase_id` int,
  `side_name` text,
  `artwork_url` text,
  `color` text,
  FOREIGN KEY (testcase_id) REFERENCES `MockupSampleTestcase` (testcase_id) on delete cascade
);
CREATE TABLE IF NOT EXISTS `SizePriceSampleTestcase` (
  `id` int PRIMARY KEY,
  `testcase_id` int,
  `price` float,
  FOREIGN KEY (testcase_id) REFERENCES `PriceSampleTestcase` (testcase_id) on delete cascade
);
CREATE TABLE IF NOT EXISTS `MockupSampleTestcase` (
  `id` int PRIMARY KEY,
  `product_id` int,
  `description` text,
  FOREIGN KEY (product_id) REFERENCES `Product` (product_id) on delete cascade
);
CREATE TABLE IF NOT EXISTS `PriceSampleTestcase` (
  `id` int PRIMARY KEY,
  `product_id` int,
  FOREIGN KEY (product_id) REFERENCES `Product` (product_id) on delete cascade
);