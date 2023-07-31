-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： localhost
-- 產生時間： 2023 年 07 月 30 日 17:17
-- 伺服器版本： 10.4.28-MariaDB
-- PHP 版本： 8.1.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `test`
--

-- --------------------------------------------------------

--
-- 資料表結構 `album`
--

CREATE TABLE `album` (
  `id` bigint(20) NOT NULL,
  `artist` varchar(100) NOT NULL,
  `desc` varchar(100) NOT NULL,
  `title` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `album`
--

INSERT INTO `album` (`id`, `artist`, `desc`, `title`) VALUES
(48, 'NoPartyForCaoDong草東沒有派對', '測試', 'NoPartyForCaoDong草東沒有派對'),
(49, '大象體操ElephantGym', '測試', '大象體操ElephantGym'),
(50, '落差草原WWWW・PrairieWWWW', '測試', '落差草原WWWW・PrairieWWWW'),
(51, 'Dr.Dre', '測試', 'Dr.Dre'),
(52, '羽毛不飘才怪', '測試', '羽毛不飘才怪'),
(53, 'BANGTANTV', '測試', 'BANGTANTV'),
(54, 'BLACKPINK', '測試', 'BLACKPINK'),
(55, '1theK(원더케이)', '測試', '1theK(원더케이)'),
(56, 'BillieEilish', '測試', 'BillieEilish'),
(57, 'officialpsy', '測試', 'officialpsy'),
(58, 'kpopifyxolarsun', '測試', 'kpopifyxolarsun'),
(59, 'HYBELABELS', '測試', 'HYBELABELS'),
(60, '湖南卫视芒果TV官方频道ChinaHunanTVOfficialChannel', '測試', '湖南卫视芒果TV官方频道ChinaHunanTVOfficialChannel'),
(61, 'BlackSabbath', '測試', 'BlackSabbath'),
(62, 'JustinJohnson', '測試', 'JustinJohnson'),
(63, 'SMTOWN', '測試', 'SMTOWN'),
(64, 'CLOfficialChannel', '測試', 'CLOfficialChannel'),
(65, '4Minute포미닛(OfficialYouTubeChannel)', '測試', '4Minute포미닛(OfficialYouTubeChannel)'),
(66, 'JYPEntertainment', '測試', 'JYPEntertainment'),
(67, 'Voiy', '測試', 'Voiy'),
(68, 'BlondieMusicOfficial', '測試', 'BlondieMusicOfficial'),
(69, 'AuntieSoul34', '測試', 'AuntieSoul34'),
(70, 'MLB', '測試', 'MLB'),
(71, 'TheBandPerry', '測試', 'TheBandPerry'),
(72, 'Boston', '測試', 'Boston'),
(73, 'BoyzIIMen', '測試', 'BoyzIIMen'),
(74, 'STMPDRCRDS', '測試', 'STMPDRCRDS'),
(75, '鏡新聞', '測試', '鏡新聞'),
(76, 'RHINO', '測試', 'RHINO'),
(77, 'GameSpot', '測試', 'GameSpot'),
(78, 'AllmanBrothersBand', '測試', 'AllmanBrothersBand'),
(79, 'SBSMandarin官方中字', '測試', 'SBSMandarin官方中字'),
(80, '東森新聞CH51', '測試', '東森新聞CH51'),
(81, '선미SUNMI', '測試', '선미SUNMI'),
(82, 'HyunA', '測試', 'HyunA'),
(83, 'UPROXXIndieMixtape', '測試', 'UPROXXIndieMixtape'),
(84, 'NCTDREAM', '測試', 'NCTDREAM'),
(85, 'WayV', '測試', 'WayV'),
(86, 'elvecindariocalle13', '測試', 'elvecindariocalle13'),
(87, 'MONSTAX', '測試', 'MONSTAX'),
(88, 'TheChemicalBrothers', '測試', 'TheChemicalBrothers'),
(89, 'StrayKids', '測試', 'StrayKids'),
(90, 'ChicagoBand', '測試', 'ChicagoBand'),
(91, 'MAMAMOO', '測試', 'MAMAMOO'),
(92, 'TheClash', '測試', 'TheClash'),
(93, 'KQENTERTAINMENT', '測試', 'KQENTERTAINMENT'),
(94, 'OfficialAliceCooper', '測試', 'OfficialAliceCooper'),
(95, '周杰倫JayChou', '測試', '周杰倫JayChou'),
(96, '(G)I-DLE(여자)아이들(OfficialYouTubeChannel)', '測試', '(G)I-DLE(여자)아이들(OfficialYouTubeChannel)'),
(97, '蔡依林JolinTsai', '測試', '蔡依林JolinTsai'),
(98, 'dutchmanmm', '測試', 'dutchmanmm'),
(99, 'illrec', '測試', 'illrec'),
(100, '여자친구GFRIENDOFFICIAL', '測試', '여자친구GFRIENDOFFICIAL'),
(101, '三立新聞網SETN', '測試', '三立新聞網SETN'),
(102, 'alper', '測試', 'alper'),
(103, 'TVBSNEWS', '測試', 'TVBSNEWS'),
(104, 'TEEPR推一波', '測試', 'TEEPR推一波'),
(105, 'Wu-TangClan', '測試', 'Wu-TangClan'),
(106, 'CreedenceClearwaterRevival', '測試', 'CreedenceClearwaterRevival'),
(107, 'KennyChesney', '測試', 'KennyChesney'),
(108, 'LongBeachFinest', '測試', 'LongBeachFinest'),
(109, 'Jaeguchi', '測試', 'Jaeguchi'),
(110, 'AadJuijn', '測試', 'AadJuijn'),
(111, 'friDay影音-潮流日韓劇、綜藝及齊全電影。每日更新。', '測試', 'friDay影音-潮流日韓劇、綜藝及齊全電影。每日更新。'),
(112, 'TheCrosbys', '測試', 'TheCrosbys'),
(113, 'DaftPunk', '測試', 'DaftPunk'),
(114, 'WeAreDeLaSoul', '測試', 'WeAreDeLaSoul'),
(118, 'hybe labels', '熱門推薦', 'hot'),
(119, 'jyp entertainment', '熱門推薦', 'hot'),
(120, '88rising', '熱門推薦', 'hot'),
(121, '玖壹壹', '熱門推薦', 'hot'),
(122, 'jung kook - tic', '熱門推薦', 'hot'),
(123, 'starshiptv', '熱門推薦', 'hot'),
(124, '伍佰 wu bai & china blue', '熱門推薦', 'hot'),
(125, 'eason chan', '熱門推薦', 'hot'),
(126, 'cai ya - tic', '熱門推薦', 'hot'),
(127, 'the first take', '熱門推薦', 'hot'),
(128, '陶喆 david tao', '熱門推薦', 'hot'),
(129, 'feng ze邱鋒澤', '熱門推薦', 'hot'),
(130, 'oh my girl', '熱門推薦', 'hot'),
(131, '3d entertainment', '熱門推薦', 'hot'),
(132, 'zerobaseone', '熱門推薦', 'hot'),
(133, 'kenshi yonezu  米津玄師', '熱門推薦', 'hot'),
(134, '徐暐翔vash hsu', '熱門推薦', 'hot'),
(135, '豪記唱片 hcm ', '熱門推薦', 'hot');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `album`
--
ALTER TABLE `album`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `album_artist_4677c6ac_uniq` (`artist`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `album`
--
ALTER TABLE `album`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=136;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
