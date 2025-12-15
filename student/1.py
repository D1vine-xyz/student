use master
go
IF DB_ID('QLSanXuat') IS NOT NULL
BEGIN
    ALTER DATABASE QLSanXuat SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE QLSanXuat;
END
GO

CREATE DATABASE QLSanXuat;
GO

USE QLSanXuat;
GO
-- Bảng Loại sản phẩm
CREATE TABLE Loai (
    MaLoai CHAR(5) NOT NULL PRIMARY KEY,
    TenLoai NVARCHAR(50) NOT NULL
);

-- Bảng Sản phẩm
CREATE TABLE SanPham (
    MaSP CHAR(5) NOT NULL PRIMARY KEY,
    TenSP NVARCHAR(100) NOT NULL,
    MaLoai CHAR(5) NOT NULL,
    FOREIGN KEY (MaLoai) REFERENCES Loai(MaLoai)
);

-- Bảng Nhân viên
CREATE TABLE NhanVien (
    MaNV CHAR(5) NOT NULL PRIMARY KEY,
    HoTen NVARCHAR(100) NOT NULL,
    NgaySinh DATE,
    Phai BIT,                -- 1: Nam | 0: Nữ
);

-- Bảng Phiếu xuất
CREATE TABLE PhieuXuat (
    MaPX CHAR(6) NOT NULL PRIMARY KEY,
    NgayLap DATE NOT NULL,
    MaNV CHAR(5) NOT NULL,
    FOREIGN KEY (MaNV) REFERENCES NhanVien(MaNV)
);

-- Bảng chi tiết phiếu xuất (Bảng liên kết nhiều-nhiều)
CREATE TABLE CTPX (
    MaPX CHAR(6) NOT NULL,
    MaSP CHAR(5) NOT NULL,
    SoLuong INT NOT NULL CHECK (SoLuong > 0),

    PRIMARY KEY (MaPX, MaSP),
    FOREIGN KEY (MaPX) REFERENCES PhieuXuat(MaPX),
    FOREIGN KEY (MaSP) REFERENCES SanPham(MaSP)
);


INSERT INTO Loai (MaLoai, TenLoai)
VALUES
('1', N'Vật liệu xây dựng'),
('2', N'Hàng tiêu dùng'),
('3', N'Ngũ cốc');


INSERT INTO SanPham (MaSP, TenSP, MaLoai) VALUES
(1, 'Xi măng', 1),
(2, 'Gạch', 1),
(3, 'gạo nàng hương', 3),
(4, 'Bột mì', 3),
(5, 'Kệ chén', 2),
(6, 'Đậu xanh', 3);

INSERT INTO NhanVien (MaNV, HoTen, NgaySinh, Phai)
VALUES
('NV01', N'Nguyễn Mai Thi', '1982-05-15', 0),
('NV02', N'Trần Đình Chiến', '1980-12-02', 1),
('NV03', N'Lê Thị Chi', '1979-01-23', 0);
('NV04', N'Huỳnh Nguyễn Trung Hiếu', '1998-06-09', 1);

INSERT INTO PhieuXuat (MaPX, NgayLap, MaNV)
VALUES
('1', '2010-03-12', 'NV01'),
('2', '2010-02-03', 'NV02'),
('3', '2010-06-01', 'NV03'),
('4', '2010-06-16', 'NV01');


INSERT INTO CTPX (MaPX, MaSP, SoLuong)
VALUES
('1', '1', 10),
('1', '2', 15),
('1', '3', 5),
('2', '2', 20),
('3', '1', 20),
('3', '3', 25),
('4', '5', 12);

SELECT * FROM Loai
SELECT * FROM SanPham
SELECT * FROM NhanVien
SELECT * FROM PhieuXuat
SELECT * FROM CTPX



--
--    BÀI TẬP   --
--
------------------------------------------------------------
-- 1. View: Tổng số lượng xuất của từng sản phẩm trong 2010
------------------------------------------------------------
CREATE VIEW V1 AS
SELECT 
    sp.MaSP,
    sp.TenSP,
    SUM(ct.SoLuong) AS TongSoLuong
FROM CTPX ct
JOIN PhieuXuat px ON ct.MaPX = px.MaPX
JOIN SanPham sp ON ct.MaSP = sp.MaSP
WHERE YEAR(px.NgayLap) = 2010
GROUP BY sp.MaSP, sp.TenSP;

-- Lấy dữ liệu sắp xếp theo tên sản phẩm
SELECT * FROM V1
ORDER BY TenSP ASC;


------------------------------------------------------------
-- 2. View: sản phẩm bán từ 1/1/2010 đến 30/6/2010
------------------------------------------------------------
CREATE VIEW V2 AS
SELECT DISTINCT
    sp.MaSP,
    sp.TenSP,
    l.TenLoai
FROM CTPX ct
JOIN PhieuXuat px ON ct.MaPX = px.MaPX
JOIN SanPham sp ON ct.MaSP = sp.MaSP
JOIN Loai l ON sp.MaLoai = l.MaLoai
WHERE px.NgayLap BETWEEN '2010-01-01' AND '2010-06-30';
SELECT * FROM V2


------------------------------------------------------------
-- 3. View: Số lượng sản phẩm theo từng loại
------------------------------------------------------------
CREATE VIEW V3 AS
SELECT 
    l.MaLoai,
    l.TenLoai,
    COUNT(sp.MaSP) AS SoLuongSanPham
FROM Loai l
LEFT JOIN SanPham sp ON l.MaLoai = sp.MaLoai
GROUP BY l.MaLoai, l.TenLoai;
SELECT * FROM V3


------------------------------------------------------------
-- 4. Tổng số phiếu xuất trong tháng 6/2010
------------------------------------------------------------
SELECT COUNT(*) AS TongPX_T6_2010
FROM PhieuXuat
WHERE YEAR(NgayLap) = 2010 AND MONTH(NgayLap) = 6;


------------------------------------------------------------
-- 5. Thông tin phiếu xuất của nhân viên NV01
------------------------------------------------------------
SELECT *
FROM PhieuXuat
WHERE MaNV = 'NV01';


------------------------------------------------------------
-- 6. Nhân viên nam tuổi > 25 và < 30 (tính theo năm 2010)
------------------------------------------------------------
SELECT 
    MaNV, HoTen, NgaySinh
FROM NhanVien
WHERE Phai = 1
  AND (2010 - YEAR(NgaySinh)) > 25
  AND (2010 - YEAR(NgaySinh)) < 30;


------------------------------------------------------------
-- 7. Thống kê số lượng phiếu xuất theo nhân viên
------------------------------------------------------------
SELECT 
    nv.MaNV,
    nv.HoTen,
    COUNT(px.MaPX) AS SoLuongPhieu
FROM NhanVien nv
LEFT JOIN PhieuXuat px ON nv.MaNV = px.MaNV
GROUP BY nv.MaNV, nv.HoTen;


------------------------------------------------------------
-- 8. Thống kê số lượng sản phẩm đã xuất theo từng sản phẩm
------------------------------------------------------------
SELECT 
    sp.MaSP,
    sp.TenSP,
    SUM(ct.SoLuong) AS TongSoLuong
FROM SanPham sp
JOIN CTPX ct ON sp.MaSP = ct.MaSP
GROUP BY sp.MaSP, sp.TenSP;


------------------------------------------------------------
-- 9. Nhân viên có số lượng phiếu xuất nhiều nhất
------------------------------------------------------------
SELECT TOP 1 
    nv.HoTen,
    COUNT(px.MaPX) AS SoLuongPhieu
FROM NhanVien nv
JOIN PhieuXuat px ON nv.MaNV = px.MaNV
GROUP BY nv.HoTen
ORDER BY SoLuongPhieu DESC;


------------------------------------------------------------
-- 10. Tên sản phẩm được xuất nhiều nhất năm 2010
------------------------------------------------------------
SELECT TOP 1
    sp.TenSP,
    SUM(ct.SoLuong) AS TongSoLuong
FROM SanPham sp
JOIN CTPX ct ON sp.MaSP = ct.MaSP
JOIN PhieuXuat px ON ct.MaPX = px.MaPX
WHERE YEAR(px.NgayLap) = 2010
GROUP BY sp.TenSP
ORDER BY TongSoLuong DESC;
