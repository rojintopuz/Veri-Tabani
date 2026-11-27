-- ============================================================================
-- Dosya   : db/10_varliklar/hasta.sql
-- Modul   : M1 Hasta & Muayene
-- Sahibi  : Rojin Topuz (032390078)
-- Aciklama: Hasta varlik tablosu
-- ============================================================================

CREATE TABLE hasta (
    hasta_kimlik_no CHAR(11)        NOT NULL,
    ad              VARCHAR(100)    NOT NULL,
    adres           VARCHAR(250),
    yas             SMALLINT        NOT NULL,

    CONSTRAINT pk_hasta PRIMARY KEY (hasta_kimlik_no),
    CONSTRAINT ck_hasta_kimlik_no CHECK (hasta_kimlik_no ~ '^[1-9][0-9]{10}$'),
    CONSTRAINT ck_hasta_ad CHECK (btrim(ad) <> ''),
    CONSTRAINT ck_hasta_yas CHECK (yas BETWEEN 0 AND 130)
);
