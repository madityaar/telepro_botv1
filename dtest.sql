-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 02, 2019 at 08:30 AM
-- Server version: 10.1.36-MariaDB
-- PHP Version: 7.2.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dtest`
--

-- --------------------------------------------------------

--
-- Table structure for table `mytable`
--

CREATE TABLE `mytable` (
  `ODP` varchar(15) NOT NULL,
  `TICKET_ID` varchar(10) NOT NULL,
  `PHOTO_BEFORE` varchar(30) DEFAULT NULL,
  `PHOTO_PROCESS` varchar(30) DEFAULT NULL,
  `PHOTO_AFTER` varchar(30) DEFAULT NULL,
  `LONGITUDE` decimal(12,8) NOT NULL,
  `LATITUDE` decimal(12,9) NOT NULL,
  `LONGITUDE_U` decimal(12,8) DEFAULT NULL,
  `LATITUDE_U` decimal(12,9) DEFAULT NULL,
  `DISTANCE` decimal(12,8) DEFAULT NULL,
  `UPDATED_BY` varchar(30) DEFAULT NULL,
  `UPDATED_DATE` varchar(30) DEFAULT NULL,
  `KETERANGAN` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `mytable`
--

INSERT INTO `mytable` (`ODP`, `TICKET_ID`, `PHOTO_BEFORE`, `PHOTO_PROCESS`, `PHOTO_AFTER`, `LONGITUDE`, `LATITUDE`, `LONGITUDE_U`, `LATITUDE_U`, `DISTANCE`, `UPDATED_BY`, `UPDATED_DATE`, `KETERANGAN`) VALUES
('ODP-BJM-FAH/020', 'IN47251082', 'IN47251082-a', 'IN47251082-b', 'IN47251082-c', '114.59021146', '-3.312957899', '106.81800900', '106.818009000', '9999.99999999', '779884734', '2019-06-28 17:11:47', 'keterangan'),
('ODP-BJM-FAL/016', 'IN47116287', NULL, NULL, NULL, '114.57293500', '-3.334448000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-BJM-FAM/038', 'IN47303491', NULL, NULL, NULL, '114.57635171', '-3.322087376', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-CIL-FAC/10', 'IN47284664', NULL, NULL, NULL, '106.92026701', '-6.117966971', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-CKC-FH/01', 'IN47306283', NULL, NULL, NULL, '108.59290000', '-6.755600000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-CPP-FDH/57', 'IN47278224', NULL, NULL, NULL, '106.86495882', '-6.174991583', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-DMO-FDN/48', 'IN47293640', NULL, NULL, NULL, '112.72400835', '-7.252937201', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-DMO-FML/21', 'IN47293832', NULL, NULL, NULL, '112.73134552', '-7.254425589', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-DMO-FPS/07', 'IN47117795', NULL, NULL, NULL, '112.73755476', '-7.289909754', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-DMO-FQZ/38', 'IN47234566', NULL, NULL, NULL, '112.71632739', '-7.284547292', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-GSK-FF/47', 'IN47292346', NULL, NULL, NULL, '112.58210000', '-7.167400000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-GTL-FAD/08', 'IN47252499', NULL, NULL, NULL, '123.07620000', '0.560800000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-GTL-FAJ/21', 'IN47246790', NULL, NULL, NULL, '123.06130000', '0.547400000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-HAR-FAR/15', 'IN47208220', NULL, NULL, NULL, '107.95739400', '-6.416139000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-IDI-FRE/01', 'IN47117599', NULL, NULL, NULL, '97.83498300', '4.883789000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-KLI-FAC/02', 'IN47242295', NULL, NULL, NULL, '107.33970000', '-6.341400000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-KMY-FH/147', 'IN47215796', NULL, NULL, NULL, '106.85472575', '-6.147087431', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-KNG-FA/14', 'IN47205288', NULL, NULL, NULL, '108.61070000', '-6.978064000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-KRT-FAL/048', 'IN47286611', NULL, NULL, NULL, '110.79740000', '-7.546900000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-KRT-FAP/048', 'IN47316109', NULL, NULL, NULL, '110.81874999', '-7.539983922', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-KRW-FAL/117', 'IN47150118', NULL, NULL, NULL, '107.28703271', '-6.336028686', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-KUD-FG/08', 'IN47278384', NULL, NULL, NULL, '110.80410000', '-6.797500000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-KWA-FAH/15', 'IN47127318', NULL, NULL, NULL, '107.31340000', '-6.312100000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-KWA-FBF/20', 'IN47129172', NULL, NULL, NULL, '107.30390000', '-6.308700000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-KWA-FBF/23', 'IN47129801', NULL, NULL, NULL, '107.30130000', '-6.309300000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-LBG-FBG/02', 'IN47307980', NULL, NULL, NULL, '107.60320000', '-6.907200000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-LBG-FBQ/52', 'IN47308090', NULL, NULL, NULL, '107.62640000', '-6.917600000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-LBG-FBR/28', 'IN47308108', NULL, NULL, NULL, '107.61540000', '-6.913700000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-LBG-FBR/65', 'IN47308194', NULL, NULL, NULL, '107.61710000', '-6.911400000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-LBG-FGG/032', 'IN47271893', NULL, NULL, NULL, '107.62793509', '-6.900223581', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-MG-FAA14', 'IN47269656', NULL, NULL, NULL, '110.23560000', '-7.414200000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-MJP-FG/050', 'IN47291611', NULL, NULL, NULL, '110.44717158', '-7.010387857', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-MRD-FN/14', 'IN47116109', NULL, NULL, NULL, '106.95693900', '-6.124911000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-MYR-FWQ/03', 'IN47317279', NULL, NULL, NULL, '112.77853600', '-7.271608580', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-PAB-FAS/01', 'IN47131946', NULL, NULL, NULL, '108.72690000', '-6.813100000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-PKL-FCG/012', 'IN47264992', NULL, NULL, NULL, '109.65658900', '-6.927784000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-PSN-FC/37', 'IN47292969', NULL, NULL, NULL, '112.88041000', '-7.645210000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-PWT-FAX/078', 'IN47249209', NULL, NULL, NULL, '109.25185952', '-7.405033366', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-PWT-FBE/080', 'IN47293635', NULL, NULL, NULL, '109.24721253', '-7.430970810', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-PWT-FS/022', 'IN47233815', NULL, NULL, NULL, '109.11238600', '-7.273010000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-SDY-FJ/02', 'IN47293241', NULL, NULL, NULL, '112.55436100', '-6.914211000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-SGR-FAK/01', 'IN47116161', NULL, NULL, NULL, '115.12700000', '-8.090100000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-SKJ-FBW/03', 'IN47315877', NULL, NULL, NULL, '106.83603792', '-6.393612161', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-SMT-FBB/009', 'IN47293964', NULL, NULL, NULL, '110.39570000', '-6.967100000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-TLE-FBH/028', 'IN47308336', NULL, NULL, NULL, '107.61470000', '-6.963700000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-TLJ-FBD/053', 'IN47287000', NULL, NULL, NULL, '107.30244115', '-6.339892612', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-TLJ-FBE/01', 'IN47242764', NULL, NULL, NULL, '107.30000000', '-6.328100000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-TLJ-FCJ/044', 'IN47226112', NULL, NULL, NULL, '107.28069060', '-6.325850157', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-TRG-FCN/107', 'IN47310688', NULL, NULL, NULL, '107.64420000', '-6.937600000', NULL, NULL, NULL, NULL, NULL, NULL),
('ODP-UBU-FN/21', 'IN47264398', NULL, NULL, NULL, '115.24934491', '-8.516889729', NULL, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `userapproval`
--

CREATE TABLE `userapproval` (
  `idUserApproval` varchar(10) NOT NULL,
  `NIK` varchar(15) NOT NULL,
  `Nama` varchar(50) NOT NULL,
  `lokasikerja` varchar(15) NOT NULL,
  `isApproved` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `userapproval`
--

INSERT INTO `userapproval` (`idUserApproval`, `NIK`, `Nama`, `lokasikerja`, `isApproved`) VALUES
('779884734', '123213', 'ADITYA', 'BDG', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `mytable`
--
ALTER TABLE `mytable`
  ADD PRIMARY KEY (`ODP`);

--
-- Indexes for table `userapproval`
--
ALTER TABLE `userapproval`
  ADD PRIMARY KEY (`idUserApproval`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
