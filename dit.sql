SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de datos: `dit`
--
DROP DATABASE IF EXISTS `dit`;
CREATE DATABASE `dit` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
USE `dit`;
GRANT ALL PRIVILEGES ON  `dit` . * TO  'dit'@'localhost' WITH GRANT OPTION ;
-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `api`
--

CREATE TABLE IF NOT EXISTS `api` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `url` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `category`
--

CREATE TABLE IF NOT EXISTS `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `place`
--

CREATE TABLE IF NOT EXISTS `place` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `address` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `categoryid` int(11) NOT NULL,
  `description` text COLLATE utf8_unicode_ci,
  `lat` double NOT NULL,
  `lng` double NOT NULL,
  `image` varchar(100) COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`categoryid`) REFERENCES category(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

--
-- Category inserts 
--

INSERT INTO category (name) VALUES ('Food'), ('Hangouts'), ('Leisure'), ('Personal care'), ('Religion'), ('Shopping');


--
-- Test inserts 
--

INSERT INTO place (name, address, categoryid, description, lat, lng, image) VALUES ('Mesón Casa Pedro', 'Calle de Asturias, 39, 33004, Oviedo', 1, 'Descripción de Mesón Casa Pedro', 43.364256, -5.856516, 'http://mesoncasapedro.es/components/com_fpss/images/cachopo2.jpg');

INSERT INTO place (name, address, categoryid, description, lat, lng, image) VALUES ('Confitería Cafetería Santa Cristina', 'Calle Uría, 43, 33003, Oviedo', 2, 'Descripción de Cafetería Santa Cristina', 43.365861, -5.854309, 'http://www.pasteleriasantacristina.es/images/Fachada-2.jpg');

INSERT INTO place (name, address, categoryid, description, lat, lng, image) VALUES ('Cines Los Prados', 'Avenida Fernández Ladreda, s/n, 33011, Oviedo', 3, 'Descripción de Cines Los Prados', 43.370894, -5.831764, 'http://www.yelmocines.es/sites/default/files/styles/cinema_gallery_full/public/p8030518.jpg');

INSERT INTO place (name, address, categoryid, description, lat, lng, image) VALUES ('Go Fit Oviedo', 'Calle Asturcón, 23, 33006, Oviedo', 4, 'Descripción de gimnasioo Go Fit Oviedo', 43.352958, -5.861082, 'http://www.yelmocines.es/sites/default/files/styles/cinema_gallery_full/public/p8030518.jpg');

INSERT INTO place (name, address, categoryid, description, lat, lng, image) VALUES ('Catedral de Oviedo', 'Plaza de Alfonso II El Casto, 33003, Oviedo', 5, 'Descripción de Catedral de Oviedo', 43.362493, -5.843607, 'http://taxicaminosantiago.com/wp-content/uploads/2013/04/Etapa1-camino-primitivo-2');

INSERT INTO place (name, address, categoryid, description, lat, lng, image) VALUES ('Centro Comercial Modoo', 'Calle Arturo Álvarez Buylla, 5, 33005, Oviedo', 6, 'Descripción de Centro Comercial Modoo', 43.358466, -5.86089, 'http://esphoto980x880.mnstatic.com/centro-comercial-modoo_5700641.jpg');



