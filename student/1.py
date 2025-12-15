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

/*
------------------------------------------------------------
--                  TẠO CÁC FUNCTION
------------------------------------------------------------
*/

-- 1. Function F1: Tổng số lượng xuất kho của tên sản phẩm trong năm
CREATE FUNCTION F1 (@TenSP NVARCHAR(100), @Nam INT)
RETURNS INT
AS
BEGIN
    DECLARE @TongSoLuong INT;

    SELECT @TongSoLuong = SUM(ct.SoLuong)
    FROM SanPham sp
    JOIN CTPX ct ON sp.MaSP = ct.MaSP
    JOIN PhieuXuat px ON ct.MaPX = px.MaPX
    WHERE sp.TenSP = @TenSP
      AND YEAR(px.NgayLap) = @Nam;

    IF @TongSoLuong IS NULL
        SET @TongSoLuong = 0;

    RETURN @TongSoLuong;
END
GO

-- 2. Function F2: Tổng số lượng phiếu xuất của nhân viên
CREATE FUNCTION F2 (@MaNV CHAR(5))
RETURNS INT
AS
BEGIN
    DECLARE @SoLuongPhieu INT;

    IF NOT EXISTS (SELECT 1 FROM NhanVien WHERE MaNV = @MaNV)
        SET @SoLuongPhieu = 0;
    ELSE
        SELECT @SoLuongPhieu = COUNT(MaPX)
        FROM PhieuXuat
        WHERE MaNV = @MaNV;

    RETURN @SoLuongPhieu;
END
GO

-- 3. Function F3: Danh sách các sản phẩm được xuất trong năm
CREATE FUNCTION F3 (@Nam INT)
RETURNS TABLE
AS
RETURN
(
    SELECT DISTINCT
        sp.MaSP,
        sp.TenSP,
        l.TenLoai
    FROM SanPham sp
    JOIN CTPX ct ON sp.MaSP = ct.MaSP
    JOIN PhieuXuat px ON ct.MaPX = px.MaPX
    JOIN Loai l ON sp.MaLoai = l.MaLoai
    WHERE YEAR(px.NgayLap) = @Nam
);
GO

-- 4. Function F4: Danh sách các phiếu xuất của nhân viên
CREATE FUNCTION F4 (@MaNV CHAR(5))
RETURNS TABLE
AS
RETURN
(
    SELECT
        MaPX,
        NgayLap,
        MaNV
    FROM PhieuXuat
    WHERE MaNV = @MaNV OR @MaNV IS NULL OR @MaNV = ''
);
GO

-- 5. Function F5: Chi tiết xuất của một phiếu xuất
CREATE FUNCTION F5 (@MaPX CHAR(6))
RETURNS TABLE
AS
RETURN
(
    SELECT
        ct.MaSP,
        sp.TenSP,
        ct.SoLuong
    FROM CTPX ct
    JOIN SanPham sp ON ct.MaSP = sp.MaSP
    WHERE ct.MaPX = @MaPX
);
GO

-- 6. Function F6: Danh sách các phiếu xuất từ ngày T1 đến T2
CREATE FUNCTION F6 (@T1 DATE, @T2 DATE)
RETURNS TABLE
AS
RETURN
(
    SELECT
        MaPX,
        NgayLap,
        MaNV
    FROM PhieuXuat
    WHERE NgayLap BETWEEN @T1 AND @T2
);
GO

-- 7. Function F7: Chi tiết phiếu xuất với một mã phiếu xuất (Giống F5)
CREATE FUNCTION F7 (@MaPX CHAR(6))
RETURNS TABLE
AS
RETURN
(
    SELECT
        ct.MaSP,
        sp.TenSP,
        ct.SoLuong
    FROM CTPX ct
    JOIN SanPham sp ON ct.MaSP = sp.MaSP
    WHERE ct.MaPX = @MaPX
);
GO


/*
------------------------------------------------------------
--                  TẠO CÁC PROCEDURE
------------------------------------------------------------
*/

-- 1. Procedure P1: Tổng số lượng xuất kho của sản phẩm trong năm 2010 (Sử dụng Function F1)
CREATE PROCEDURE P1
    @TenSP NVARCHAR(100),
    @TongSoLuong INT OUTPUT
AS
BEGIN
    SELECT @TongSoLuong = dbo.F1(@TenSP, 2010);
END
GO

-- 2. Procedure P2: Tổng số lượng xuất kho của sản phẩm từ 4/2010 đến 6/2010
CREATE PROCEDURE P2
    @TenSP NVARCHAR(100),
    @TongSoLuong INT OUTPUT
AS
BEGIN
    SELECT @TongSoLuong = SUM(ct.SoLuong)
    FROM SanPham sp
    JOIN CTPX ct ON sp.MaSP = ct.MaSP
    JOIN PhieuXuat px ON ct.MaPX = px.MaPX
    WHERE sp.TenSP = @TenSP
      AND px.NgayLap BETWEEN '2010-04-01' AND '2010-06-30';

    IF @TongSoLuong IS NULL
    BEGIN
        SET @TongSoLuong = 0;
    END
END
GO

-- 3. Procedure P3: Số lượng xuất kho của sản phẩm từ 4/2010 đến 6/2010 (GỌI Procedure P2)
CREATE PROCEDURE P3
    @TenSP NVARCHAR(100)
AS
BEGIN
    DECLARE @SoLuongXuat INT;

    EXEC P2 @TenSP = @TenSP, @TongSoLuong = @SoLuongXuat OUTPUT;

    SELECT
        @TenSP AS TenSanPham,
        N'4/2010 đến 6/2010' AS KhoangThoiGian,
        @SoLuongXuat AS TongSoLuongXuat;
END
GO

-- 4. Procedure P4: INSERT record vào bảng Loai
CREATE PROCEDURE P4
    @MaLoai CHAR(5),
    @TenLoai NVARCHAR(50)
AS
BEGIN
    IF EXISTS (SELECT 1 FROM Loai WHERE MaLoai = @MaLoai)
    BEGIN
        RAISERROR(N'Mã loại đã tồn tại. Không thể thêm.', 16, 1);
        RETURN;
    END

    INSERT INTO Loai (MaLoai, TenLoai)
    VALUES (@MaLoai, @TenLoai);

    SELECT N'Thêm loại sản phẩm thành công!' AS ThongBao;
END
GO

-- 5. Procedure P5: DELETE record từ bảng NhanVien
CREATE PROCEDURE P5
    @MaNV CHAR(5)
AS
BEGIN
    IF EXISTS (SELECT 1 FROM PhieuXuat WHERE MaNV = @MaNV)
    BEGIN
        RAISERROR(N'Không thể xóa nhân viên này vì có phiếu xuất liên quan.', 16, 1);
        RETURN;
    END

    IF NOT EXISTS (SELECT 1 FROM NhanVien WHERE MaNV = @MaNV)
    BEGIN
        RAISERROR(N'Mã nhân viên không tồn tại.', 16, 1);
        RETURN;
    END

    DELETE FROM NhanVien
    WHERE MaNV = @MaNV;

    SELECT N'Xóa nhân viên thành công!' AS ThongBao;
END
GO------------------------------------------------------------
-- 1. Trigger T1: Giới hạn số phiếu xuất (Tối đa 5 phiếu/ngày/NV)
------------------------------------------------------------
CREATE TRIGGER T1_KiemTraSoPhieuXuat
ON PhieuXuat
FOR INSERT
AS
BEGIN
    DECLARE @MaNV CHAR(5);
    DECLARE @NgayLap DATE;
    DECLARE @SoPhieuDaLap INT;
    
    -- Lấy thông tin từ phiếu vừa được INSERT
    SELECT @MaNV = MaNV, @NgayLap = NgayLap FROM inserted;

    -- Đếm số lượng phiếu xuất đã lập của nhân viên đó trong cùng ngày (bao gồm cả phiếu vừa INSERT)
    SELECT @SoPhieuDaLap = COUNT(MaPX)
    FROM PhieuXuat
    WHERE MaNV = @MaNV 
      AND NgayLap = @NgayLap;

    -- Nếu số lượng lớn hơn 5, HỦY thao tác INSERT
    IF @SoPhieuDaLap > 5
    BEGIN
        RAISERROR(N'Lỗi: Mỗi nhân viên chỉ được lập tối đa 5 phiếu xuất trong một ngày.', 16, 1);
        ROLLBACK TRANSACTION;
    END
END
GO

 ------------------------------------------------------------
-- 2. Trigger T2: Giới hạn số chi tiết phiếu xuất (Tối đa 10 chi tiết/phiếu)
------------------------------------------------------------
CREATE TRIGGER T2_KiemTraSoCTPX
ON CTPX
FOR INSERT
AS
BEGIN
    DECLARE @MaPX CHAR(6);
    DECLARE @SoChiTiet INT;

    -- Lấy MaPX của chi tiết vừa được INSERT
    SELECT @MaPX = MaPX FROM inserted;

    -- Đếm số chi tiết hiện có của phiếu đó (bao gồm cả chi tiết vừa INSERT)
    SELECT @SoChiTiet = COUNT(MaSP)
    FROM CTPX
    WHERE MaPX = @MaPX;

    -- Nếu số lượng lớn hơn 10, HỦY thao tác INSERT
    IF @SoChiTiet > 10
    BEGIN
        RAISERROR(N'Lỗi: Mỗi phiếu xuất chỉ được có tối đa 10 chi tiết (dòng sản phẩm) khác nhau.', 16, 1);
        ROLLBACK TRANSACTION;
    END
END
GO------------------------------------------------------------
-- 3. Trigger T3: Kiểm tra Mã PX có tồn tại trong CTPX
------------------------------------------------------------
CREATE TRIGGER T3_KiemTraMaPX_CTPX
ON CTPX
FOR INSERT
AS
BEGIN
    -- Kiểm tra xem có bất kỳ MaPX nào trong bảng 'inserted' (dữ liệu mới) 
    -- mà KHÔNG tồn tại trong bảng 'PhieuXuat'
    IF EXISTS (
        SELECT i.MaPX
        FROM inserted i
        LEFT JOIN PhieuXuat px ON i.MaPX = px.MaPX
        WHERE px.MaPX IS NULL
    )
    BEGIN
        RAISERROR(N'Lỗi: Mã phiếu xuất trong chi tiết phiếu xuất không tồn tại trong bảng PhieuXuat.', 16, 1);
        ROLLBACK TRANSACTION;
    END
END
GO




