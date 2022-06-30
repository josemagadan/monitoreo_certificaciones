# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 10:41:44 2022

@author: jose.magadan
"""

consultas_sql = {
'TELEFONOS_INVALIDOS': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_TIPOTELEFONO = 0 THEN 1 ELSE 0 END)/count(*) AS invalido
        , SUM(CASE WHEN CLV_TIPOTELEFONO = 1 THEN 1 ELSE 0 END)/count(*) AS casa_valido
        , SUM(CASE WHEN CLV_TIPOTELEFONO = 2 THEN 1 ELSE 0 END)/count(*) AS celular_valido
        , SUM(CASE WHEN CLV_TIPOTELEFONO = 3 THEN 1 ELSE 0 END)/count(*) AS casa_celular_validos
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_TIPOTELEFONO = 0 THEN 1 ELSE 0 END)/count(*) AS invalido
        , SUM(CASE WHEN CLV_TIPOTELEFONO = 1 THEN 1 ELSE 0 END)/count(*) AS casa_valido
        , SUM(CASE WHEN CLV_TIPOTELEFONO = 2 THEN 1 ELSE 0 END)/count(*) AS celular_valido
        , SUM(CASE WHEN CLV_TIPOTELEFONO = 3 THEN 1 ELSE 0 END)/count(*) AS casa_celular_validos
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE ((FEC_MOVIMIENTO <= '20201020' AND FEC_MOVIMIENTO >= '20200804') OR FEC_MOVIMIENTO <= '20200420')
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha, INVALIDO, p.mediana, p.mediana + 2*p.desviacion AS l_sup, (CASE WHEN (p.mediana - 2*p.desviacion < 0) then 0 else (p.mediana - 2*p.desviacion) END) AS l_inf
        FROM tmp, (SELECT PERCENTILE_CONT(0.5) WITHIN group (ORDER BY INVALIDO) AS mediana, stddev_pop(invalido) AS desviacion FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
        
'PARENTESCO': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_PARENTESCOREFERENCIA = 'A' THEN 1 ELSE 0 END)/count(*) AS ABUELO
        , SUM(CASE WHEN CLV_PARENTESCOREFERENCIA = 'B' THEN 1 ELSE 0 END)/count(*) AS SOBRINO
        , SUM(CASE WHEN CLV_PARENTESCOREFERENCIA = 'E' THEN 1 ELSE 0 END)/count(*) AS CONYUGE
        , SUM(CASE WHEN CLV_PARENTESCOREFERENCIA = 'H' THEN 1 ELSE 0 END)/count(*) AS HERMANO
        , SUM(CASE WHEN CLV_PARENTESCOREFERENCIA = 'I' THEN 1 ELSE 0 END)/count(*) AS AMIGO
        , SUM(CASE WHEN CLV_PARENTESCOREFERENCIA = 'J' THEN 1 ELSE 0 END)/count(*) AS HIJO
        , SUM(CASE WHEN CLV_PARENTESCOREFERENCIA = 'P' THEN 1 ELSE 0 END)/count(*) AS PADRE
        , SUM(CASE WHEN CLV_PARENTESCOREFERENCIA = 'R' THEN 1 ELSE 0 END)/count(*) AS PRIMO
        , SUM(CASE WHEN CLV_PARENTESCOREFERENCIA = 'T' THEN 1 ELSE 0 END)/count(*) AS TIO
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000 AND CLV_PARENTESCOREFERENCIA != ''
        GROUP BY fecha, dia
        ORDER BY fecha), 
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_PARENTESCOREFERENCIA = 'A' THEN 1 ELSE 0 END)/count(*) AS ABUELO
        , SUM(CASE WHEN CLV_PARENTESCOREFERENCIA = 'B' THEN 1 ELSE 0 END)/count(*) AS SOBRINO
        , SUM(CASE WHEN CLV_PARENTESCOREFERENCIA = 'E' THEN 1 ELSE 0 END)/count(*) AS CONYUGE
        , SUM(CASE WHEN CLV_PARENTESCOREFERENCIA = 'H' THEN 1 ELSE 0 END)/count(*) AS HERMANO
        , SUM(CASE WHEN CLV_PARENTESCOREFERENCIA = 'I' THEN 1 ELSE 0 END)/count(*) AS AMIGO
        , SUM(CASE WHEN CLV_PARENTESCOREFERENCIA = 'J' THEN 1 ELSE 0 END)/count(*) AS HIJO
        , SUM(CASE WHEN CLV_PARENTESCOREFERENCIA = 'P' THEN 1 ELSE 0 END)/count(*) AS PADRE
        , SUM(CASE WHEN CLV_PARENTESCOREFERENCIA = 'R' THEN 1 ELSE 0 END)/count(*) AS PRIMO
        , SUM(CASE WHEN CLV_PARENTESCOREFERENCIA = 'T' THEN 1 ELSE 0 END)/count(*) AS TIO
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= '20210824' AND FEC_MOVIMIENTO <= '20211006'
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000 AND CLV_PARENTESCOREFERENCIA != ''
        GROUP BY fecha, dia
        )
        SELECT fecha, ABUELO, p.mediana_a AS mediana, .04 AS l_sup, 0 AS l_inf,
        SOBRINO, p.mediana_b AS mediana, .04 AS l_sup, 0 AS l_inf,
        CONYUGE, p.mediana_e AS mediana, p.mediana_e + 3*p.desviacion_e AS l_sup, p.mediana_e - 3*p.desviacion_e AS l_inf,
        HERMANO, p.mediana_h AS mediana, p.mediana_h + 3*p.desviacion_h AS l_sup, p.mediana_h - 3*p.desviacion_h AS l_inf,
        AMIGO, p.mediana_i AS mediana, p.mediana_i + 3*p.desviacion_i AS l_sup, p.mediana_i - 3*p.desviacion_i AS l_inf,
        HIJO, p.mediana_j AS mediana, .06 AS l_sup, .01 AS l_inf, 
        PADRE, p.mediana_p AS mediana, p.mediana_p + 3*p.desviacion_p AS l_sup, p.mediana_p - 3*p.desviacion_p AS l_inf,
        PRIMO, p.mediana_r AS mediana, .06 AS l_sup, .01 AS l_inf,
        TIO, p.mediana_t AS mediana, .06 AS l_sup, .01 AS l_inf
        FROM tmp, 
        (SELECT PERCENTILE_CONT(0.5) WITHIN group (ORDER BY ABUELO) AS mediana_a, stddev_pop(ABUELO) AS desviacion_a
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY SOBRINO) AS mediana_b, stddev_pop(SOBRINO) AS desviacion_b
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY CONYUGE) AS mediana_e, stddev_pop(CONYUGE) AS desviacion_e
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY HERMANO) AS mediana_h, stddev_pop(HERMANO) AS desviacion_h
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY AMIGO) AS mediana_i, stddev_pop(AMIGO) AS desviacion_i
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY HIJO) AS mediana_j, stddev_pop(HIJO) AS desviacion_j
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY PADRE) AS mediana_p, stddev_pop(PADRE) AS desviacion_p
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY PRIMO) AS mediana_r, stddev_pop(PRIMO) AS desviacion_r
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY TIO) AS mediana_t, stddev_pop(TIO) AS desviacion_t
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
        
'CANAL_SOLICITUD': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_CANALSOLICITUD = 1 THEN 1 ELSE 0 END)/count(*) AS tienda
        , SUM(CASE WHEN CLV_CANALSOLICITUD = 2 THEN 1 ELSE 0 END)/count(*) AS calle
        , SUM(CASE WHEN CLV_CANALSOLICITUD in (3,4) THEN 1 ELSE 0 END)/count(*) AS web
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_CANALSOLICITUD = 1 THEN 1 ELSE 0 END)/count(*) AS tienda
        , SUM(CASE WHEN CLV_CANALSOLICITUD = 2 THEN 1 ELSE 0 END)/count(*) AS calle
        , SUM(CASE WHEN CLV_CANALSOLICITUD in (3,4) THEN 1 ELSE 0 END)/count(*) AS web
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO > '20220218' AND FEC_MOVIMIENTO <= '20220418'
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , tienda, p.mediana_t, p.mediana_t + 3*p.desviacion_t AS l_sup, p.mediana_t - 3*p.desviacion_t AS l_inf
        , calle, p.mediana_c, p.mediana_c + 3*p.desviacion_c AS l_sup, p.mediana_c - 3*p.desviacion_c AS l_inf
        , web, p.mediana_w, p.mediana_w + 3*p.desviacion_w AS l_sup, p.mediana_w - 3*p.desviacion_w AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY tienda) AS mediana_t, stddev_pop(tienda) AS desviacion_t
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY calle) AS mediana_c, stddev_pop(calle) AS desviacion_c
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY web) AS mediana_w, stddev_pop(web) AS desviacion_w
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
        
'ESCOLARIDAD': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_ESCOLARIDAD = '1' THEN 1 ELSE 0 END)/count(*) AS no_estudio
        , SUM(CASE WHEN CLV_ESCOLARIDAD = '2' THEN 1 ELSE 0 END)/count(*) AS primaria
        , SUM(CASE WHEN CLV_ESCOLARIDAD = '3' THEN 1 ELSE 0 END)/count(*) AS secundaria
        , SUM(CASE WHEN CLV_ESCOLARIDAD = '4' THEN 1 ELSE 0 END)/count(*) AS carrera_tecnica
        , SUM(CASE WHEN CLV_ESCOLARIDAD = '5' THEN 1 ELSE 0 END)/count(*) AS preparatoria
        , SUM(CASE WHEN CLV_ESCOLARIDAD = '6' THEN 1 ELSE 0 END)/count(*) AS profesional
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_ESCOLARIDAD = '1' THEN 1 ELSE 0 END)/count(*) AS no_estudio
        , SUM(CASE WHEN CLV_ESCOLARIDAD = '2' THEN 1 ELSE 0 END)/count(*) AS primaria
        , SUM(CASE WHEN CLV_ESCOLARIDAD = '3' THEN 1 ELSE 0 END)/count(*) AS secundaria
        , SUM(CASE WHEN CLV_ESCOLARIDAD = '4' THEN 1 ELSE 0 END)/count(*) AS carrera_tecnica
        , SUM(CASE WHEN CLV_ESCOLARIDAD = '5' THEN 1 ELSE 0 END)/count(*) AS preparatoria
        , SUM(CASE WHEN CLV_ESCOLARIDAD = '6' THEN 1 ELSE 0 END)/count(*) AS profesional
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= '20210830' AND FEC_MOVIMIENTO <= '20211006'
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , no_estudio, p.mediana_ne, p.mediana_ne + 3*p.desviacion_ne AS l_sup, p.mediana_ne - 3*p.desviacion_ne AS l_inf
        , primaria, p.mediana_p, p.mediana_p + 3*p.desviacion_p AS l_sup, p.mediana_p - 3*p.desviacion_p AS l_inf
        , secundaria, p.mediana_s, p.mediana_s + 3*p.desviacion_s AS l_sup, p.mediana_s - 3*p.desviacion_s AS l_inf
        , carrera_tecnica, p.mediana_ct, p.mediana_ct + 3*p.desviacion_ct AS l_sup, p.mediana_ct - 3*p.desviacion_ct AS l_inf
        , preparatoria, p.mediana_pp, p.mediana_pp + 3*p.desviacion_pp AS l_sup, p.mediana_pp - 3*p.desviacion_pp AS l_inf
        , profesional, p.mediana_pf, p.mediana_pf + 3*p.desviacion_pf AS l_sup, p.mediana_pf - 3*p.desviacion_pf AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY no_estudio) AS mediana_ne, stddev_pop(no_estudio) AS desviacion_ne
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY primaria) AS mediana_p, stddev_pop(primaria) AS desviacion_p
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY secundaria) AS mediana_s, stddev_pop(secundaria) AS desviacion_s
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY carrera_tecnica) AS mediana_ct, stddev_pop(carrera_tecnica) AS desviacion_ct
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY preparatoria) AS mediana_pp, stddev_pop(preparatoria) AS desviacion_pp
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY profesional) AS mediana_pf, stddev_pop(profesional) AS desviacion_pf
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'ESTADO_CIVL': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_ESTADOCIVIL = 'S' THEN 1 ELSE 0 END)/count(*) AS soltero
        , SUM(CASE WHEN CLV_ESTADOCIVIL = 'U' THEN 1 ELSE 0 END)/count(*) AS union_libre
        , SUM(CASE WHEN CLV_ESTADOCIVIL = 'D' THEN 1 ELSE 0 END)/count(*) AS divorciado
        , SUM(CASE WHEN CLV_ESTADOCIVIL = 'V' THEN 1 ELSE 0 END)/count(*) AS viudo
        , SUM(CASE WHEN CLV_ESTADOCIVIL = 'C' THEN 1 ELSE 0 END)/count(*) AS casado
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_ESTADOCIVIL = 'S' THEN 1 ELSE 0 END)/count(*) AS soltero
        , SUM(CASE WHEN CLV_ESTADOCIVIL = 'U' THEN 1 ELSE 0 END)/count(*) AS union_libre
        , SUM(CASE WHEN CLV_ESTADOCIVIL = 'D' THEN 1 ELSE 0 END)/count(*) AS divorciado
        , SUM(CASE WHEN CLV_ESTADOCIVIL = 'V' THEN 1 ELSE 0 END)/count(*) AS viudo
        , SUM(CASE WHEN CLV_ESTADOCIVIL = 'C' THEN 1 ELSE 0 END)/count(*) AS casado
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= '20210824' AND FEC_MOVIMIENTO <= '20211006'
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , soltero, p.mediana_s, p.mediana_s + 3*p.desviacion_s AS l_sup, p.mediana_s - 3*p.desviacion_s AS l_inf
        , union_libre, p.mediana_ul, p.mediana_ul + 3*p.desviacion_ul AS l_sup, p.mediana_ul - 3*p.desviacion_ul AS l_inf
        , divorciado, p.mediana_d, p.mediana_d + 3*p.desviacion_d AS l_sup, p.mediana_d - 3*p.desviacion_d AS l_inf
        , viudo, p.mediana_v, p.mediana_v + 3*p.desviacion_v AS l_sup, p.mediana_v - 3*p.desviacion_v AS l_inf
        , casado, p.mediana_c, p.mediana_c + 3*p.desviacion_c AS l_sup, p.mediana_c - 3*p.desviacion_c AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY soltero) AS mediana_s, stddev_pop(soltero) AS desviacion_s
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY union_libre) AS mediana_ul, stddev_pop(union_libre) AS desviacion_ul
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY divorciado) AS mediana_d, stddev_pop(divorciado) AS desviacion_d
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY viudo) AS mediana_v, stddev_pop(viudo) AS desviacion_v
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY casado) AS mediana_c, stddev_pop(casado) AS desviacion_c
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'GRUPO_EVALUACION': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN NUM_GRUPOEVALUACION = 1 THEN 1 ELSE 0 END)/count(*) AS uno
        , SUM(CASE WHEN NUM_GRUPOEVALUACION = 2 THEN 1 ELSE 0 END)/count(*) AS dos
        , SUM(CASE WHEN NUM_GRUPOEVALUACION = 3 THEN 1 ELSE 0 END)/count(*) AS tres
        , SUM(CASE WHEN NUM_GRUPOEVALUACION = 4 THEN 1 ELSE 0 END)/count(*) AS cuatro
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN NUM_GRUPOEVALUACION = 1 THEN 1 ELSE 0 END)/count(*) AS uno
        , SUM(CASE WHEN NUM_GRUPOEVALUACION = 2 THEN 1 ELSE 0 END)/count(*) AS dos
        , SUM(CASE WHEN NUM_GRUPOEVALUACION = 3 THEN 1 ELSE 0 END)/count(*) AS tres
        , SUM(CASE WHEN NUM_GRUPOEVALUACION = 4 THEN 1 ELSE 0 END)/count(*) AS cuatro
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= '20200412'
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , uno, p.mediana_1, (CASE WHEN (p.mediana_1 + 3*p.desviacion_1 > 1) then 1 else (p.mediana_1 + 3*p.desviacion_1) END) AS l_sup, (CASE WHEN (p.mediana_1 - 3*p.desviacion_1 < 0) then 0 else (p.mediana_1 - 3*p.desviacion_1) END) AS l_inf
        , dos, p.mediana_2, (CASE WHEN (p.mediana_2 + 3*p.desviacion_2 > 1) then 1 else (p.mediana_2 + 3*p.desviacion_2) END) AS l_sup, (CASE WHEN (p.mediana_2 - 3*p.desviacion_2 < 0) then 0 else (p.mediana_2 - 3*p.desviacion_2) END) AS l_inf
        , tres, p.mediana_3, (CASE WHEN (p.mediana_3 + 3*p.desviacion_3 > 1) then 1 else (p.mediana_3 + 3*p.desviacion_3) END) AS l_sup, (CASE WHEN (p.mediana_3 - 3*p.desviacion_3 < 0) then 0 else (p.mediana_3 - 3*p.desviacion_3) END) AS l_inf
        , cuatro, p.mediana_4, (CASE WHEN (p.mediana_4 + 3*p.desviacion_4 > 1) then 1 else (p.mediana_4 + 3*p.desviacion_4) END) AS l_sup, (CASE WHEN (p.mediana_4 - 3*p.desviacion_4 < 0) then 0 else (p.mediana_4 - 3*p.desviacion_4) END) AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY uno) AS mediana_1, stddev_pop(uno) AS desviacion_1
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY dos) AS mediana_2, stddev_pop(dos) AS desviacion_2
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY tres) AS mediana_3, stddev_pop(tres) AS desviacion_3
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY cuatro) AS mediana_4, stddev_pop(cuatro) AS desviacion_4
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'TIPO_CASA': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_TIPOCASA = 'P' THEN 1 ELSE 0 END)/count(*) AS propia
        , SUM(CASE WHEN CLV_TIPOCASA = 'G' THEN 1 ELSE 0 END)/count(*) AS pagandola
        , SUM(CASE WHEN CLV_TIPOCASA = 'R' THEN 1 ELSE 0 END)/count(*) AS rentada
        , SUM(CASE WHEN CLV_TIPOCASA = 'F' THEN 1 ELSE 0 END)/count(*) AS familiar
        , SUM(CASE WHEN CLV_TIPOCASA = 'H' THEN 1 ELSE 0 END)/count(*) AS huesped
        , SUM(CASE WHEN CLV_TIPOCASA = 'D' THEN 1 ELSE 0 END)/count(*) AS prestada
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_TIPOCASA = 'P' THEN 1 ELSE 0 END)/count(*) AS propia
        , SUM(CASE WHEN CLV_TIPOCASA = 'G' THEN 1 ELSE 0 END)/count(*) AS pagandola
        , SUM(CASE WHEN CLV_TIPOCASA = 'R' THEN 1 ELSE 0 END)/count(*) AS rentada
        , SUM(CASE WHEN CLV_TIPOCASA = 'F' THEN 1 ELSE 0 END)/count(*) AS familiar
        , SUM(CASE WHEN CLV_TIPOCASA = 'H' THEN 1 ELSE 0 END)/count(*) AS huesped
        , SUM(CASE WHEN CLV_TIPOCASA = 'D' THEN 1 ELSE 0 END)/count(*) AS prestada
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= '20210824' AND FEC_MOVIMIENTO <= '20211006'
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , propia, p.mediana_p, p.mediana_p + 3*p.desviacion_p AS l_sup, p.mediana_p - 3*p.desviacion_p AS l_inf
        , pagandola, p.mediana_g, p.mediana_g + 0.005 AS l_sup, 0 AS l_inf
        , rentada, p.mediana_r, p.mediana_r + 3*p.desviacion_r AS l_sup, p.mediana_r - 3*p.desviacion_r AS l_inf
        , familiar, p.mediana_f, p.mediana_f + 3*p.desviacion_f AS l_sup, p.mediana_f - 3*p.desviacion_f AS l_inf
        , huesped, p.mediana_h, p.mediana_h + 0.005 AS l_sup, 0 AS l_inf
        , prestada, p.mediana_d, p.mediana_d + 3*p.desviacion_d AS l_sup, p.mediana_d - 3*p.desviacion_d AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY propia) AS mediana_p, stddev_pop(propia) AS desviacion_p
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY pagandola) AS mediana_g, stddev_pop(pagandola) AS desviacion_g
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY rentada) AS mediana_r, stddev_pop(rentada) AS desviacion_r
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY familiar) AS mediana_f, stddev_pop(familiar) AS desviacion_f
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY huesped) AS mediana_h, stddev_pop(huesped) AS desviacion_h
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY prestada) AS mediana_d, stddev_pop(prestada) AS desviacion_d
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'TIPO_CONSULTA': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_TIPOCONSULTA = 'NC' THEN 1 ELSE 0 END)/count(*) AS no_consulto
        , SUM(CASE WHEN CLV_TIPOCONSULTA = 'CC' THEN 1 ELSE 0 END)/count(*) AS circulo
        , SUM(CASE WHEN CLV_TIPOCONSULTA = 'BC' THEN 1 ELSE 0 END)/count(*) AS buro
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_TIPOCONSULTA = 'NC' THEN 1 ELSE 0 END)/count(*) AS no_consulto
        , SUM(CASE WHEN CLV_TIPOCONSULTA = 'CC' THEN 1 ELSE 0 END)/count(*) AS circulo
        , SUM(CASE WHEN CLV_TIPOCONSULTA = 'BC' THEN 1 ELSE 0 END)/count(*) AS buro
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= '20211005' AND FEC_MOVIMIENTO <= '20211110'
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , NO_CONSULTO, p.mediana_n, p.mediana_n + 3*p.desviacion_n AS l_sup, p.mediana_n - 3*p.desviacion_n AS l_inf
        , CIRCULO, p.mediana_c, p.mediana_c + 3*p.desviacion_c AS l_sup, p.mediana_c - 3*p.desviacion_c AS l_inf
        , BURO, p.mediana_b, p.mediana_b + 3*p.desviacion_b AS l_sup, p.mediana_b - 3*p.desviacion_b AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY NO_CONSULTO) AS mediana_n, stddev_pop(NO_CONSULTO) AS desviacion_n
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY CIRCULO) AS mediana_c, stddev_pop(CIRCULO) AS desviacion_c
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY BURO) AS mediana_b, stddev_pop(BURO) AS desviacion_b
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'TIPO_PROSPECTO': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_FLAGPROSPECTO = '' THEN 1 ELSE 0 END)/count(*) AS no_prospecto
        , SUM(CASE WHEN CLV_FLAGPROSPECTO = '1' THEN 1 ELSE 0 END)/count(*) AS p_normal
        , SUM(CASE WHEN CLV_FLAGPROSPECTO = '2' THEN 1 ELSE 0 END)/count(*) AS p_sin_documentacion
        , SUM(CASE WHEN CLV_FLAGPROSPECTO = '3' THEN 1 ELSE 0 END)/count(*) AS p_por_cobranza
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        and NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_FLAGPROSPECTO = '' THEN 1 ELSE 0 END)/count(*) AS no_prospecto
        , SUM(CASE WHEN CLV_FLAGPROSPECTO = '1' THEN 1 ELSE 0 END)/count(*) AS p_normal
        , SUM(CASE WHEN CLV_FLAGPROSPECTO = '2' THEN 1 ELSE 0 END)/count(*) AS p_sin_documentacion
        , SUM(CASE WHEN CLV_FLAGPROSPECTO = '3' THEN 1 ELSE 0 END)/count(*) AS p_por_cobranza
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE date(FEC_MOVIMIENTO) between '20210822' and '20211022'
        and NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , no_prospecto, p.mediana_np, p.mediana_np + 2*p.desviacion_np AS l_sup, p.mediana_np - 2*p.desviacion_np AS l_inf
        , P_NORMAL, p.mediana_n, p.mediana_n + 2*p.desviacion_n AS l_sup, p.mediana_n - 2*p.desviacion_n AS l_inf
        , P_SIN_DOCUMENTACION, p.mediana_sd, p.mediana_sd + .002 AS l_sup, 0 AS l_inf
        , P_POR_COBRANZA, p.mediana_c, p.mediana_c + 2*p.desviacion_c AS l_sup, p.mediana_c - 2*p.desviacion_c AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY NO_PROSPECTO ) AS mediana_np, stddev_pop(NO_PROSPECTO ) AS desviacion_np
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY P_NORMAL ) AS mediana_n, stddev_pop(P_NORMAL ) AS desviacion_n
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY P_SIN_DOCUMENTACION ) AS mediana_sd, stddev_pop(P_SIN_DOCUMENTACION) AS desviacion_sd
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY P_POR_COBRANZA ) AS mediana_c, stddev_pop(P_POR_COBRANZA) AS desviacion_c
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'PRODUCTO_BANCO': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_PRODUCTOBANCO = '6001' THEN 1 ELSE 0 END)/count(*) AS bancoppel_visa
        , SUM(CASE WHEN CLV_PRODUCTOBANCO = '' THEN 1 ELSE 0 END)/count(*) AS sin_producto
        , SUM(CASE WHEN CLV_PRODUCTOBANCO in ('6600','8500','6400','7800','6500','7600','7700','6300','6800') THEN 1 ELSE 0 END)/count(*) AS otros
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_PRODUCTOBANCO = '6001' THEN 1 ELSE 0 END)/count(*) AS bancoppel_visa
        , SUM(CASE WHEN CLV_PRODUCTOBANCO = '' THEN 1 ELSE 0 END)/count(*) AS sin_producto
        , SUM(CASE WHEN CLV_PRODUCTOBANCO in ('6600','8500','6400','7800','6500','7600','7700','6300','6800') THEN 1 ELSE 0 END)/count(*) AS otros
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= '20211005' AND FEC_MOVIMIENTO <= '20211231'
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , bancoppel_visa, p.mediana_visa, p.mediana_visa + 3*p.desviacion_visa AS l_sup, p.mediana_visa - 3*p.desviacion_visa AS l_inf
        , sin_producto, p.mediana_sin, p.mediana_sin + 3*p.desviacion_sin AS l_sup, p.mediana_sin - 3*p.desviacion_sin AS l_inf
        , otros, p.mediana_otros, p.mediana_otros + 3*p.desviacion_otros AS l_sup, p.mediana_otros - 3*p.desviacion_otros AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY bancoppel_visa ) AS mediana_visa, stddev_pop(bancoppel_visa ) AS desviacion_visa
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY sin_producto ) AS mediana_sin, stddev_pop(sin_producto) AS desviacion_sin
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY otros ) AS mediana_otros, stddev_pop(otros) AS desviacion_otros
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'ESTATUS_BANCO': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_ESTATUSSOLICITUDBANCO in ('PA','AT','AP') THEN 1 ELSE 0 END)/count(*) AS autorizadas
        , SUM(CASE WHEN CLV_ESTATUSSOLICITUDBANCO in ('CM','RT','RP') THEN 1 ELSE 0 END)/count(*) AS rechazadas
        , SUM(CASE WHEN CLV_ESTATUSSOLICITUDBANCO in ('MC','EE','OS','LC','CE','OA','EA') THEN 1 ELSE 0 END)/count(*) AS orden_supervision
        , SUM(CASE WHEN CLV_ESTATUSSOLICITUDBANCO in ('AN','PC','RA','CN','CV','EC','BC','CC','ST') THEN 1 ELSE 0 END)/count(*) AS pendientes
        , SUM(CASE WHEN CLV_ESTATUSSOLICITUDBANCO = '' THEN 1 ELSE 0 END)/count(*) AS sin_estatus
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_ESTATUSSOLICITUDBANCO in ('PA','AT','AP') THEN 1 ELSE 0 END)/count(*) AS autorizadas
        , SUM(CASE WHEN CLV_ESTATUSSOLICITUDBANCO in ('CM','RT','RP') THEN 1 ELSE 0 END)/count(*) AS rechazadas
        , SUM(CASE WHEN CLV_ESTATUSSOLICITUDBANCO in ('MC','EE','OS','LC','CE','OA','EA') THEN 1 ELSE 0 END)/count(*) AS orden_supervision
        , SUM(CASE WHEN CLV_ESTATUSSOLICITUDBANCO in ('AN','PC','RA','CN','CV','EC','BC','CC','ST') THEN 1 ELSE 0 END)/count(*) AS pendientes
        , SUM(CASE WHEN CLV_ESTATUSSOLICITUDBANCO = '' THEN 1 ELSE 0 END)/count(*) AS sin_estatus
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= '20220510' AND FEC_MOVIMIENTO <= '20220810'
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , AUTORIZADAS , p.mediana_a, p.mediana_a + 3*p.desviacion_a AS l_sup, 0 AS l_inf
        , RECHAZADAS , p.mediana_r, p.mediana_r + 3*p.desviacion_r AS l_sup, p.mediana_r - 3*p.desviacion_r AS l_inf
        , ORDEN_SUPERVISION , p.mediana_os, p.mediana_os + 3*p.desviacion_os AS l_sup, p.mediana_os - 3*p.desviacion_os AS l_inf
        , PENDIENTES , p.mediana_p, p.mediana_p + 3*p.desviacion_p AS l_sup, p.mediana_p - 3*p.desviacion_p AS l_inf
        , SIN_ESTATUS , p.mediana_sin, p.mediana_sin + 3*p.desviacion_sin AS l_sup, p.mediana_sin - 3*p.desviacion_sin AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY AUTORIZADAS) AS mediana_a, stddev_pop(AUTORIZADAS ) AS desviacion_a
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY RECHAZADAS ) AS mediana_r, stddev_pop(RECHAZADAS ) AS desviacion_r
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY ORDEN_SUPERVISION ) AS mediana_os, stddev_pop(ORDEN_SUPERVISION ) AS desviacion_os
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY PENDIENTES ) AS mediana_p, stddev_pop(PENDIENTES ) AS desviacion_p
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY SIN_ESTATUS ) AS mediana_sin, stddev_pop(SIN_ESTATUS ) AS desviacion_sin
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'DIVISIONES': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN s.DIVISIONTDA = 'DIVISION 1' THEN 1 ELSE 0 END)/count(*) AS division1
        , SUM(CASE WHEN s.DIVISIONTDA = 'DIVISION 2' THEN 1 ELSE 0 END)/count(*) AS division2
        , SUM(CASE WHEN s.DIVISIONTDA = 'DIVISION 3' THEN 1 ELSE 0 END)/count(*) AS division3
        , SUM(CASE WHEN s.DIVISIONTDA = 'DIVISION 4' THEN 1 ELSE 0 END)/count(*) AS division4
        , SUM(CASE WHEN s.DIVISIONTDA = 'DIVISION 5' THEN 1 ELSE 0 END)/count(*) AS division5
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES p
        INNER JOIN (select idtienda AS sucursal, divisiontda from VentaRM.Mexico.CatTienda where FechaCorte='2020-12-31'
        AND DIVISIONTDA != '' ORDER BY 1) s on cast(p.NUM_SUCURSALSOLICITUD AS integer) = s.sucursal
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN s.DIVISIONTDA = 'DIVISION 1' THEN 1 ELSE 0 END)/count(*) AS division1
        , SUM(CASE WHEN s.DIVISIONTDA = 'DIVISION 2' THEN 1 ELSE 0 END)/count(*) AS division2
        , SUM(CASE WHEN s.DIVISIONTDA = 'DIVISION 3' THEN 1 ELSE 0 END)/count(*) AS division3
        , SUM(CASE WHEN s.DIVISIONTDA = 'DIVISION 4' THEN 1 ELSE 0 END)/count(*) AS division4
        , SUM(CASE WHEN s.DIVISIONTDA = 'DIVISION 5' THEN 1 ELSE 0 END)/count(*) AS division5
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES p
        INNER JOIN (select idtienda AS sucursal, divisiontda from VentaRM.Mexico.CatTienda where FechaCorte='2020-12-31'
        AND DIVISIONTDA != '' ORDER BY 1) s on cast(p.NUM_SUCURSALSOLICITUD AS integer) = s.sucursal
        WHERE FEC_MOVIMIENTO > '20200801'
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , division1 , p.mediana_1, p.mediana_1 + 3*p.desviacion_1 AS l_sup, p.mediana_1 - 3*p.desviacion_1 AS l_inf
        , division2 , p.mediana_2, p.mediana_2 + 3*p.desviacion_2 AS l_sup, p.mediana_2 - 3*p.desviacion_2 AS l_inf
        , division3 , p.mediana_3, p.mediana_3 + 3*p.desviacion_3 AS l_sup, p.mediana_3 - 3*p.desviacion_3 AS l_inf
        , division4 , p.mediana_4, p.mediana_4 + 3*p.desviacion_4 AS l_sup, p.mediana_4 - 3*p.desviacion_4 AS l_inf
        , division5 , p.mediana_5, p.mediana_5 + 3*p.desviacion_5 AS l_sup, p.mediana_5 - 3*p.desviacion_5 AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY division1) AS mediana_1, stddev_pop(division1 ) AS desviacion_1
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY division2 ) AS mediana_2, stddev_pop(division2 ) AS desviacion_2
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY division3 ) AS mediana_3, stddev_pop(division3 ) AS desviacion_3
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY division4 ) AS mediana_4, stddev_pop(division4 ) AS desviacion_4
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY division5 ) AS mediana_5, stddev_pop(division5 ) AS desviacion_5
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'NUMERICAS': """
        select * from ( WITH tmp AS 
        (SELECT  
        DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , avg(CASE WHEN NUM_GRUPOHIT = 2 AND num_consultasbanco >= 0 THEN num_consultasbanco END) AS consultas_banco
        , avg(CASE WHEN NUM_GRUPOHIT = 2 AND num_consultascomunicaciones >= 0 THEN num_consultascomunicaciones END) AS consultados_comunicaciones
        , avg(CASE WHEN NUM_GRUPOHIT = 2 AND num_consultasfinanciera >= 0 THEN num_consultasfinanciera END) AS consultas_financiera
        , avg(CASE WHEN NUM_GRUPOHIT = 2 AND num_consultassic >= 0 THEN num_consultassic END) AS consultas_sic
        , avg(CASE WHEN NUM_GRUPOHIT = 2 AND num_consultasmuebles >= 0 THEN num_consultasmuebles END) AS consultas_muebles
        , avg(CASE WHEN NUM_GRUPOHIT = 2 AND num_consultasprestamos >= 0 THEN num_consultasprestamos END) AS consultas_prestamos
        , avg(CASE WHEN NUM_GRUPOHIT = 2 AND num_consultasndiashitsininformacion >= 0 THEN num_consultasndiashitsininformacion END) AS consultas_hitSin
        , avg(CASE WHEN NUM_GRUPOHIT = 2 AND num_consultastarjetasndias >= 0 THEN num_consultastarjetasndias END) AS consultas_tarjetas
        , avg(CASE WHEN NUM_GRUPOHIT = 2 AND num_direccionesreportadasndias >= 0 THEN num_direccionesreportadasndias END) AS direcciones_reportadas
        , avg(CASE WHEN NUM_GRUPOHIT = 3 AND num_consultasndiashitconinformacion >= 0 THEN num_consultasndiashitconinformacion END) AS consultas_hitCon
        , avg(CASE WHEN NUM_GRUPOHIT = 3 AND num_vecesbancoppel >= 0 THEN num_vecesbancoppel END) AS num_vecesbancoppel
        , avg(CASE WHEN NUM_GRUPOHIT = 3 AND num_vecestiendacomercial >= 0 THEN num_vecestiendacomercial END) AS num_vecestiendacomercial 
        , avg(CASE WHEN NUM_GRUPOHIT = 3 AND num_vecesarrendamiento >= 0 THEN num_vecesarrendamiento END) AS num_vecesarrendamiento
        , avg(CASE WHEN NUM_GRUPOHIT = 3 AND num_vecescompraauto >= 0 THEN num_vecescompraauto END) AS num_vecescompraauto
        , avg(CASE WHEN NUM_GRUPOHIT = 3 AND num_tarjetascredito >= 0 THEN num_tarjetascredito END) AS num_tarjetascredito
        , avg(CASE WHEN NUM_GRUPOHIT = 3 AND num_saldocuentasabiertas >= 0 THEN num_saldocuentasabiertas END) AS num_saldocuentasabiertas
        , avg(CASE WHEN NUM_GRUPOHIT = 3 AND num_limitecreditocuentasabiertas >= 0 THEN num_limitecreditocuentasabiertas END) AS num_limitecreditocuentasabiertas
        , avg(num_habitantesdomicilio) AS num_habitantesdomicilio
        , avg(num_dependientes) AS num_dependientes
        , avg(num_nivelingreso) AS num_nivelingreso
        , avg(CASE WHEN num_mesesantiguedadentrada >= 0 THEN num_mesesantiguedadentrada END ) AS num_mesesantiguedadentrada
        , avg(CASE WHEN NUM_GRUPOHIT = 3 AND num_peormopentrada >= 0 THEN num_peormopentrada END ) AS num_peormopentrada
        , avg(CASE WHEN num_solicitudes >= 0 THEN num_solicitudes END ) AS num_solicitudes
        , avg(num_ingreso) AS num_ingreso
        , avg(num_longitudtramaburo) AS num_longitudtramaburo
        , avg(num_trabajadoresdomicilio) AS num_trabajadoresdomicilio
        , avg(CASE WHEN CLV_ESTATUSSOLICITUDBANCO IN ('AP','PA','AT') then num_lineacreditoautorizado ELSE NULL END) AS num_lineacreditoautorizado
        , avg(CASE WHEN num_mesesantiguedad >= 0 THEN num_mesesantiguedad END ) AS num_mesesantiguedad
        , avg(CASE WHEN NUM_GRUPOHIT = 3 AND num_mesescuentareciente >=0 THEN num_mesescuentareciente END ) AS num_mesescuentareciente
        , avg(CASE WHEN NUM_GRUPOHIT = 3 AND num_mopactual >= 0 THEN num_mopactual END ) AS num_mopactual
        , avg(CASE WHEN num_direccionesreportadas >= 0 THEN num_direccionesreportadas END ) AS num_direccionesreportadas
        , avg(CASE WHEN prc_usocuentasabiertas >= 0 THEN prc_usocuentasabiertas END ) AS prc_usocuentasabiertas
        , avg(CASE WHEN num_maximoplazo >= 0 THEN num_maximoplazo END ) AS num_maximoplazo
        , avg(CASE WHEN num_mesesmopreciente >= 0 THEN num_mesesmopreciente END ) AS num_mesesmopreciente
        , avg(CASE WHEN num_mopreciente >= 0 THEN num_mopreciente END ) AS num_mopreciente
        , avg(num_saldomopreciente) AS num_saldomopreciente
        , avg(num_scoredomicilio) AS num_scoredomicilio
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY 1,2
        ORDER BY fecha),
        tmp2 as
        (SELECT date(FEC_MOVIMIENTO) AS fecha
        , avg(CASE WHEN NUM_GRUPOHIT = 2 AND num_consultasbanco >= 0 THEN num_consultasbanco END) AS consultas_banco
        , avg(CASE WHEN NUM_GRUPOHIT = 2 AND num_consultascomunicaciones >= 0 THEN num_consultascomunicaciones END) AS consultados_comunicaciones
        , avg(CASE WHEN NUM_GRUPOHIT = 2 AND num_consultasfinanciera >= 0 THEN num_consultasfinanciera END) AS consultas_financiera
        , avg(CASE WHEN NUM_GRUPOHIT = 2 AND num_consultassic >= 0 THEN num_consultassic END) AS consultas_sic
        , avg(CASE WHEN NUM_GRUPOHIT = 2 AND num_consultasmuebles >= 0 THEN num_consultasmuebles END) AS consultas_muebles
        , avg(CASE WHEN NUM_GRUPOHIT = 2 AND num_consultasprestamos >= 0 THEN num_consultasprestamos END) AS consultas_prestamos
        , avg(CASE WHEN NUM_GRUPOHIT = 2 AND num_consultasndiashitsininformacion >= 0 THEN num_consultasndiashitsininformacion END) AS consultas_hitSin
        , avg(CASE WHEN NUM_GRUPOHIT = 2 AND num_consultastarjetasndias >= 0 THEN num_consultastarjetasndias END) AS consultas_tarjetas
        , avg(CASE WHEN NUM_GRUPOHIT = 2 AND num_direccionesreportadasndias >= 0 THEN num_direccionesreportadasndias END) AS direcciones_reportadas
        , avg(CASE WHEN NUM_GRUPOHIT = 3 AND num_consultasndiashitconinformacion >= 0 THEN num_consultasndiashitconinformacion END) AS consultas_hitCon
        , avg(CASE WHEN NUM_GRUPOHIT = 3 AND num_vecesbancoppel >= 0 THEN num_vecesbancoppel END) AS num_vecesbancoppel
        , avg(CASE WHEN NUM_GRUPOHIT = 3 AND num_vecestiendacomercial >= 0 THEN num_vecestiendacomercial END) AS num_vecestiendacomercial 
        , avg(CASE WHEN NUM_GRUPOHIT = 3 AND num_vecesarrendamiento >= 0 THEN num_vecesarrendamiento END) AS num_vecesarrendamiento
        , avg(CASE WHEN NUM_GRUPOHIT = 3 AND num_vecescompraauto >= 0 THEN num_vecescompraauto END) AS num_vecescompraauto
        , avg(CASE WHEN NUM_GRUPOHIT = 3 AND num_tarjetascredito >= 0 THEN num_tarjetascredito END) AS num_tarjetascredito
        , avg(CASE WHEN NUM_GRUPOHIT = 3 AND num_saldocuentasabiertas >= 0 THEN num_saldocuentasabiertas END) AS num_saldocuentasabiertas
        , avg(CASE WHEN NUM_GRUPOHIT = 3 AND num_limitecreditocuentasabiertas >= 0 THEN num_limitecreditocuentasabiertas END) AS num_limitecreditocuentasabiertas
        , avg(num_habitantesdomicilio) AS num_habitantesdomicilio
        , avg(num_dependientes) AS num_dependientes
        , avg(num_nivelingreso) AS num_nivelingreso
        , avg(CASE WHEN num_mesesantiguedadentrada >= 0 THEN num_mesesantiguedadentrada END ) AS num_mesesantiguedadentrada
        , avg(CASE WHEN NUM_GRUPOHIT = 3 AND num_peormopentrada >= 0 THEN num_peormopentrada END ) AS num_peormopentrada
        , avg(CASE WHEN num_solicitudes >= 0 THEN num_solicitudes END ) AS num_solicitudes
        , avg(num_ingreso) AS num_ingreso
        , avg(num_longitudtramaburo) AS num_longitudtramaburo
        , avg(num_trabajadoresdomicilio) AS num_trabajadoresdomicilio
        , avg(CASE WHEN CLV_ESTATUSSOLICITUDBANCO IN ('AP','PA','AT') then num_lineacreditoautorizado ELSE NULL END) AS num_lineacreditoautorizado
        , avg(CASE WHEN num_mesesantiguedad >= 0 THEN num_mesesantiguedad END ) AS num_mesesantiguedad
        , avg(CASE WHEN NUM_GRUPOHIT = 3 AND num_mesescuentareciente >=0 THEN num_mesescuentareciente END ) AS num_mesescuentareciente
        , avg(CASE WHEN NUM_GRUPOHIT = 3 AND num_mopactual >= 0 THEN num_mopactual END ) AS num_mopactual
        , avg(CASE WHEN num_direccionesreportadas >= 0 THEN num_direccionesreportadas END ) AS num_direccionesreportadas
        , avg(CASE WHEN prc_usocuentasabiertas >= 0 THEN prc_usocuentasabiertas END ) AS prc_usocuentasabiertas
        , avg(CASE WHEN num_maximoplazo >= 0 THEN num_maximoplazo END ) AS num_maximoplazo
        , avg(CASE WHEN num_mesesmopreciente >= 0 THEN num_mesesmopreciente END ) AS num_mesesmopreciente
        , avg(CASE WHEN num_mopreciente >= 0 THEN num_mopreciente END ) AS num_mopreciente
        , avg(num_saldomopreciente) AS num_saldomopreciente
        , avg(num_scoredomicilio) AS num_scoredomicilio
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= '20220126' AND FEC_MOVIMIENTO <= '20220726'
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY 1
        ORDER BY 1)
        SELECT tmp.fecha
        , tmp.consultas_banco, avg(tmp2.consultas_banco) AS media, avg(tmp2.consultas_banco) + 3*stddev_pop(tmp2.consultas_banco) AS l_sup, avg(tmp2.consultas_banco) - 3*stddev_pop(tmp2.consultas_banco) AS l_inf
        , tmp.consultados_comunicaciones, avg(tmp2.consultados_comunicaciones) AS media, avg(tmp2.consultados_comunicaciones) + 2*stddev_pop(tmp2.consultados_comunicaciones) AS l_sup, avg(tmp2.consultados_comunicaciones) - 2*stddev_pop(tmp2.consultados_comunicaciones) AS l_inf
        , tmp.consultas_financiera, avg(tmp2.consultas_financiera) AS media, 1 AS l_sup, 0 AS l_inf
        , tmp.consultas_sic, avg(tmp2.consultas_sic) AS media, 1 AS l_sup, 0 AS l_inf
        , tmp.consultas_muebles, avg(tmp2.consultas_muebles) AS media, avg(tmp2.consultas_muebles) + 2*stddev_pop(tmp2.consultas_muebles) AS l_sup, avg(tmp2.consultas_muebles) - 2*stddev_pop(tmp2.consultas_muebles) AS l_inf
        , tmp.consultas_prestamos, avg(tmp2.consultas_prestamos) AS media, 1 AS l_sup, 0 AS l_inf
        , tmp.consultas_hitSin, avg(tmp2.consultas_hitSin) AS media, avg(tmp2.consultas_hitSin) + 1 AS l_sup, avg(tmp2.consultas_hitSin) - 1 AS l_inf
        , tmp.consultas_tarjetas, avg(tmp2.consultas_tarjetas) AS media, avg(tmp2.consultas_tarjetas) + 1 AS l_sup, avg(tmp2.consultas_tarjetas) - 1 AS l_inf
        , tmp.direcciones_reportadas, avg(tmp2.direcciones_reportadas) AS media, avg(tmp2.direcciones_reportadas) + 2*stddev_pop(tmp2.direcciones_reportadas) AS l_sup, avg(tmp2.direcciones_reportadas) - 2*stddev_pop(tmp2.direcciones_reportadas) AS l_inf
        , tmp.consultas_hitCon, avg(tmp2.consultas_hitCon) AS media, avg(tmp2.consultas_hitCon) + 1 AS l_sup, avg(tmp2.consultas_hitCon) - 1 AS l_inf
        , tmp.num_vecesbancoppel, avg(tmp2.num_vecesbancoppel) AS media, avg(tmp2.num_vecesbancoppel) + 2*stddev_pop(tmp2.num_vecesbancoppel) AS l_sup, avg(tmp2.num_vecesbancoppel) - 2*stddev_pop(tmp2.num_vecesbancoppel) AS l_inf
        , tmp.num_vecestiendacomercial, avg(tmp2.num_vecestiendacomercial) AS media, avg(tmp2.num_vecestiendacomercial) + 2*stddev_pop(tmp2.num_vecestiendacomercial) AS l_sup, avg(tmp2.num_vecestiendacomercial) - 2*stddev_pop(tmp2.num_vecestiendacomercial) AS l_inf
        , tmp.num_vecesarrendamiento, avg(tmp2.num_vecesarrendamiento) AS media, avg(tmp2.num_vecesarrendamiento) + 2*stddev_pop(tmp2.num_vecesarrendamiento) AS l_sup, avg(tmp2.num_vecesarrendamiento) - 2*stddev_pop(tmp2.num_vecesarrendamiento) AS l_inf
        , tmp.num_vecescompraauto, avg(tmp2.num_vecescompraauto) AS media, avg(tmp2.num_vecescompraauto) + 2*stddev_pop(tmp2.num_vecescompraauto) AS l_sup, avg(tmp2.num_vecescompraauto) - 2*stddev_pop(tmp2.num_vecescompraauto) AS l_inf
        , tmp.num_tarjetascredito, avg(tmp2.num_tarjetascredito) AS media, avg(tmp2.num_tarjetascredito) + 2*stddev_pop(tmp2.num_tarjetascredito) AS l_sup, avg(tmp2.num_tarjetascredito) - 2*stddev_pop(tmp2.num_tarjetascredito) AS l_inf
        , tmp.num_saldocuentasabiertas, avg(tmp2.num_saldocuentasabiertas) AS media, avg(tmp2.num_saldocuentasabiertas) + 2*stddev_pop(tmp2.num_saldocuentasabiertas) AS l_sup, avg(tmp2.num_saldocuentasabiertas) - 2*stddev_pop(tmp2.num_saldocuentasabiertas) AS l_inf
        , tmp.num_limitecreditocuentasabiertas, avg(tmp2.num_limitecreditocuentasabiertas) AS media, avg(tmp2.num_limitecreditocuentasabiertas) + 2*stddev_pop(tmp2.num_limitecreditocuentasabiertas) AS l_sup, avg(tmp2.num_limitecreditocuentasabiertas) - 2*stddev_pop(tmp2.num_limitecreditocuentasabiertas) AS l_inf
        , tmp.num_habitantesdomicilio, avg(tmp2.num_habitantesdomicilio) AS media, avg(tmp2.num_habitantesdomicilio) + 0.5 AS l_sup, avg(tmp2.num_habitantesdomicilio) - 0.5 AS l_inf
        , tmp.num_dependientes, avg(tmp2.num_dependientes) AS media, avg(tmp2.num_dependientes) + 2*stddev_pop(tmp2.num_dependientes) AS l_sup, avg(tmp2.num_dependientes) - 2*stddev_pop(tmp2.num_dependientes) AS l_inf
        , tmp.num_nivelingreso, avg(tmp2.num_nivelingreso) AS media, avg(tmp2.num_nivelingreso) + 1 AS l_sup, avg(tmp2.num_nivelingreso) - 1 AS l_inf
        , tmp.num_mesesantiguedadentrada, avg(tmp2.num_mesesantiguedadentrada) AS media, avg(tmp2.num_mesesantiguedadentrada) + 3*stddev_pop(tmp2.num_mesesantiguedadentrada) AS l_sup, avg(tmp2.num_mesesantiguedadentrada) - 3*stddev_pop(tmp2.num_mesesantiguedadentrada) AS l_inf
        , tmp.num_peormopentrada, avg(tmp2.num_peormopentrada) AS media, avg(tmp2.num_peormopentrada) + 2*stddev_pop(tmp2.num_peormopentrada) AS l_sup, avg(tmp2.num_peormopentrada) - 2*stddev_pop(tmp2.num_peormopentrada) AS l_inf
        , tmp.num_solicitudes, avg(tmp2.num_solicitudes) AS media, avg(tmp2.num_solicitudes) + 2*stddev_pop(tmp2.num_solicitudes) AS l_sup, avg(tmp2.num_solicitudes) - 2*stddev_pop(tmp2.num_solicitudes) AS l_inf
        , tmp.num_ingreso, avg(tmp2.num_ingreso) AS media, avg(tmp2.num_ingreso) + 3*stddev_pop(tmp2.num_ingreso) AS l_sup, avg(tmp2.num_ingreso) - 3*stddev_pop(tmp2.num_ingreso) AS l_inf
        , tmp.num_longitudtramaburo, avg(tmp2.num_longitudtramaburo) AS media, avg(tmp2.num_longitudtramaburo) + 2*stddev_pop(tmp2.num_longitudtramaburo) AS l_sup, avg(tmp2.num_longitudtramaburo) - 2*stddev_pop(tmp2.num_longitudtramaburo) AS l_inf
        , tmp.num_trabajadoresdomicilio, avg(tmp2.num_trabajadoresdomicilio) AS media, avg(tmp2.num_trabajadoresdomicilio) + 2*stddev_pop(tmp2.num_trabajadoresdomicilio) AS l_sup, avg(tmp2.num_trabajadoresdomicilio) - 2*stddev_pop(tmp2.num_trabajadoresdomicilio) AS l_inf
        , tmp.num_lineacreditoautorizado, avg(tmp2.num_lineacreditoautorizado) AS media, avg(tmp2.num_lineacreditoautorizado) + 2*stddev_pop(tmp2.num_lineacreditoautorizado) AS l_sup, avg(tmp2.num_lineacreditoautorizado) - 2*stddev_pop(tmp2.num_lineacreditoautorizado) AS l_inf
        , tmp.num_mesesantiguedad, avg(tmp2.num_mesesantiguedad) AS media, avg(tmp2.num_mesesantiguedad) + 3*stddev_pop(tmp2.num_mesesantiguedad) AS l_sup, avg(tmp2.num_mesesantiguedad) - 3*stddev_pop(tmp2.num_mesesantiguedad) AS l_inf
        , tmp.num_mesescuentareciente, avg(tmp2.num_mesescuentareciente) AS media, avg(tmp2.num_mesescuentareciente) + 3*stddev_pop(tmp2.num_mesescuentareciente) AS l_sup, avg(tmp2.num_mesescuentareciente) - 3*stddev_pop(tmp2.num_mesescuentareciente) AS l_inf
        , tmp.num_mopactual, avg(tmp2.num_mopactual) AS media, avg(tmp2.num_mopactual) + 3*stddev_pop(tmp2.num_mopactual) AS l_sup, avg(tmp2.num_mopactual) - 3*stddev_pop(tmp2.num_mopactual) AS l_inf
        , tmp.num_direccionesreportadas, avg(tmp2.num_direccionesreportadas) AS media, avg(tmp2.num_direccionesreportadas) + 2*stddev_pop(tmp2.num_direccionesreportadas) AS l_sup, avg(tmp2.num_direccionesreportadas) - 2*stddev_pop(tmp2.num_direccionesreportadas) AS l_inf
        , tmp.prc_usocuentasabiertas, avg(tmp2.prc_usocuentasabiertas) AS media, avg(tmp2.prc_usocuentasabiertas) + 2*stddev_pop(tmp2.prc_usocuentasabiertas) AS l_sup, avg(tmp2.prc_usocuentasabiertas) - 2*stddev_pop(tmp2.prc_usocuentasabiertas) AS l_inf
        , tmp.num_maximoplazo, avg(tmp2.num_maximoplazo) AS media, avg(tmp2.num_maximoplazo) + 3*stddev_pop(tmp2.num_maximoplazo) AS l_sup, avg(tmp2.num_maximoplazo) - 3*stddev_pop(tmp2.num_maximoplazo) AS l_inf
        , tmp.num_mesesmopreciente, avg(tmp2.num_mesesmopreciente) AS media, avg(tmp2.num_mesesmopreciente) + 2*stddev_pop(tmp2.num_mesesmopreciente) AS l_sup, avg(tmp2.num_mesesmopreciente) - 2*stddev_pop(tmp2.num_mesesmopreciente) AS l_inf
        , tmp.num_mopreciente, avg(tmp2.num_mopreciente) AS media, avg(tmp2.num_mopreciente) + 2*stddev_pop(tmp2.num_mopreciente) AS l_sup, avg(tmp2.num_mopreciente) - 2*stddev_pop(tmp2.num_mopreciente) AS l_inf
        , tmp.num_saldomopreciente, avg(tmp2.num_saldomopreciente) AS media, avg(tmp2.num_saldomopreciente) + 2*stddev_pop(tmp2.num_saldomopreciente) AS l_sup, avg(tmp2.num_saldomopreciente) - stddev_pop(tmp2.num_saldomopreciente) AS l_inf
        , tmp.num_scoredomicilio, avg(tmp2.num_scoredomicilio) AS media, avg(tmp2.num_scoredomicilio) + 2*stddev_pop(tmp2.num_scoredomicilio) AS l_sup, avg(tmp2.num_scoredomicilio) - 2*stddev_pop(tmp2.num_scoredomicilio) AS l_inf
        FROM tmp, tmp2
        GROUP BY 1,2,6,10,14,18,22,26,30,34,38,42,46,50,54,58,62,66,70,74,78,82,86,90,94,98,102,106,110,114,118,122,126,130,134,138,142,146
        ORDER BY fecha) a order by 1
        """,
'GENERO': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_GENERO = 'F' THEN 1 ELSE 0 END)/count(*) AS femenino
        , SUM(CASE WHEN CLV_GENERO = 'M' THEN 1 ELSE 0 END)/count(*) AS masculino
        , SUM(CASE WHEN CLV_GENERO = '' THEN 1 ELSE 0 END)/count(*) AS sin_
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_GENERO = 'F' THEN 1 ELSE 0 END)/count(*) AS femenino
        , SUM(CASE WHEN CLV_GENERO = 'M' THEN 1 ELSE 0 END)/count(*) AS masculino
        , SUM(CASE WHEN CLV_GENERO = '' THEN 1 ELSE 0 END)/count(*) AS sin_
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO < '20201008'
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , femenino , p.mediana_f, p.mediana_f + 2*p.desviacion_f AS l_sup, p.mediana_f - 2*p.desviacion_f AS l_inf
        , masculino , p.mediana_m, p.mediana_m + 2*p.desviacion_m AS l_sup, p.mediana_m - 2*p.desviacion_m AS l_inf
        , sin_ , p.mediana_s, 0.01 AS l_sup, 0 AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY femenino) AS mediana_f, stddev_pop(femenino) AS desviacion_f
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY masculino ) AS mediana_m, stddev_pop(masculino ) AS desviacion_m
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY sin_ ) AS mediana_s, stddev_pop(sin_ ) AS desviacion_s
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'CREDENCIAL_ELECTOR': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN opc_credencialelector = 'S' THEN 1 ELSE 0 END)/count(*) AS S
        , SUM(CASE WHEN opc_credencialelector = 'N' THEN 1 ELSE 0 END)/count(*) AS N
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN opc_credencialelector = 'S' THEN 1 ELSE 0 END)/count(*) AS S
        , SUM(CASE WHEN opc_credencialelector = 'N' THEN 1 ELSE 0 END)/count(*) AS N
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO > '20210830' AND FEC_MOVIMIENTO < '20211006'
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , S , p.mediana_s, 1 AS l_sup, p.mediana_s - 3*p.desviacion_s AS l_inf
        , N , p.mediana_n, p.mediana_n + 3*p.desviacion_n AS l_sup, 0 AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY S) AS mediana_s, stddev_pop(S) AS desviacion_s
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY N) AS mediana_n, stddev_pop(N) AS desviacion_n
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'COMPROBANTE_DOMICILIO': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN opc_comprobantedomicilio = 'S' THEN 1 ELSE 0 END)/count(*) AS S
        , SUM(CASE WHEN opc_comprobantedomicilio = 'N' THEN 1 ELSE 0 END)/count(*) AS N
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        and NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN opc_comprobantedomicilio = 'S' THEN 1 ELSE 0 END)/count(*) AS S
        , SUM(CASE WHEN opc_comprobantedomicilio = 'N' THEN 1 ELSE 0 END)/count(*) AS N
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO > '20211005' AND FEC_MOVIMIENTO < '20211110'
        and NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , S , p.mediana_s, p.mediana_s + 2*p.desviacion_s AS l_sup, p.mediana_s - 2*p.desviacion_s AS l_inf
        , N , p.mediana_n, p.mediana_n + 2*p.desviacion_n AS l_sup, p.mediana_n - 2*p.desviacion_n AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY S) AS mediana_s, stddev_pop(S) AS desviacion_s
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY N) AS mediana_n, stddev_pop(N) AS desviacion_n
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'GRUPO_HIT': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN num_grupohit = 1 THEN 1 ELSE 0 END)/count(*) AS no_hit
        , SUM(CASE WHEN num_grupohit = 2 THEN 1 ELSE 0 END)/count(*) AS hit_sin_info
        , SUM(CASE WHEN num_grupohit = 3 THEN 1 ELSE 0 END)/count(*) AS hit_con_info
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        and NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN num_grupohit = 1 THEN 1 ELSE 0 END)/count(*) AS no_hit
        , SUM(CASE WHEN num_grupohit = 2 THEN 1 ELSE 0 END)/count(*) AS hit_sin_info
        , SUM(CASE WHEN num_grupohit = 3 THEN 1 ELSE 0 END)/count(*) AS hit_con_info
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= '20220126' AND FEC_MOVIMIENTO <= '20220326'
        and NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , no_hit, p.mediana_no, p.mediana_no + 2*p.desviacion_no AS l_sup, p.mediana_no - 2*p.desviacion_no AS l_inf
        , hit_sin_info, p.mediana_sin, p.mediana_sin + 2*p.desviacion_sin AS l_sup, p.mediana_sin - 2*p.desviacion_sin AS l_inf
        , hit_con_info, p.mediana_con, p.mediana_con + 2*p.desviacion_con AS l_sup, p.mediana_con - 2*p.desviacion_con AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY no_hit) AS mediana_no, stddev_pop(no_hit) AS desviacion_no
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY hit_sin_info) AS mediana_sin, stddev_pop(hit_sin_info) AS desviacion_sin
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY hit_con_info) AS mediana_con, stddev_pop(hit_con_info) AS desviacion_con
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'REFERENCIA_1': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN clv_puntualidadreferencia1 = 'A' THEN 1 ELSE 0 END)/count(*) AS A
        , SUM(CASE WHEN clv_puntualidadreferencia1 = 'B' THEN 1 ELSE 0 END)/count(*) AS B
        , SUM(CASE WHEN clv_puntualidadreferencia1 = 'C' THEN 1 ELSE 0 END)/count(*) AS C
        , SUM(CASE WHEN clv_puntualidadreferencia1 = 'D' THEN 1 ELSE 0 END)/count(*) AS D
        , SUM(CASE WHEN clv_puntualidadreferencia1 = 'N' THEN 1 ELSE 0 END)/count(*) AS N
        , SUM(CASE WHEN clv_puntualidadreferencia1 = 'Z' THEN 1 ELSE 0 END)/count(*) AS Z
        , SUM(CASE WHEN clv_puntualidadreferencia1 = '' THEN 1 ELSE 0 END)/count(*) AS sin_
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        and NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN clv_puntualidadreferencia1 = 'A' THEN 1 ELSE 0 END)/count(*) AS A
        , SUM(CASE WHEN clv_puntualidadreferencia1 = 'B' THEN 1 ELSE 0 END)/count(*) AS B
        , SUM(CASE WHEN clv_puntualidadreferencia1 = 'C' THEN 1 ELSE 0 END)/count(*) AS C
        , SUM(CASE WHEN clv_puntualidadreferencia1 = 'D' THEN 1 ELSE 0 END)/count(*) AS D
        , SUM(CASE WHEN clv_puntualidadreferencia1 = 'N' THEN 1 ELSE 0 END)/count(*) AS N
        , SUM(CASE WHEN clv_puntualidadreferencia1 = 'Z' THEN 1 ELSE 0 END)/count(*) AS Z
        , SUM(CASE WHEN clv_puntualidadreferencia1 = '' THEN 1 ELSE 0 END)/count(*) AS sin_
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO > '20200815'
        and NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , A, p.mediana_a, p.mediana_a + 2*p.desviacion_a AS l_sup, p.mediana_a - 2*p.desviacion_a AS l_inf
        , B, p.mediana_b, p.mediana_b + 2*p.desviacion_b AS l_sup, p.mediana_b - 2*p.desviacion_b AS l_inf
        , C, p.mediana_c, p.mediana_c + 2*p.desviacion_c AS l_sup, p.mediana_c - 2*p.desviacion_c AS l_inf
        , D, p.mediana_d, p.mediana_d + 2*p.desviacion_d AS l_sup, p.mediana_d - 2*p.desviacion_d AS l_inf
        , N, p.mediana_n, p.mediana_n + 2*p.desviacion_n AS l_sup, p.mediana_n - 2*p.desviacion_n AS l_inf
        , Z, p.mediana_z, p.mediana_z + 2*p.desviacion_z AS l_sup, p.mediana_z - 2*p.desviacion_z AS l_inf
        , sin_, p.mediana_sin, p.mediana_sin + 2*p.desviacion_sin AS l_sup, p.mediana_sin - 2*p.desviacion_sin AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY A) AS mediana_a, stddev_pop(A) AS desviacion_a
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY B) AS mediana_b, stddev_pop(B) AS desviacion_b
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY C) AS mediana_c, stddev_pop(C) AS desviacion_c
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY D) AS mediana_d, stddev_pop(D) AS desviacion_d
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY N) AS mediana_n, stddev_pop(N) AS desviacion_n
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY Z) AS mediana_z, stddev_pop(Z) AS desviacion_z
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY sin_) AS mediana_sin, stddev_pop(sin_) AS desviacion_sin
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'REFERENCIA_2': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN clv_puntualidadreferencia2 IN ('A','B','C','D','N','Z') THEN 1 ELSE 0 END)/count(*) AS con
        , SUM(CASE WHEN clv_puntualidadreferencia2 = '' THEN 1 ELSE 0 END)/count(*) AS sin_
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        and NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN clv_puntualidadreferencia2 IN ('A','B','C','D','N','Z') THEN 1 ELSE 0 END)/count(*) AS con
        , SUM(CASE WHEN clv_puntualidadreferencia2 = '' THEN 1 ELSE 0 END)/count(*) AS sin_
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO > '20200815'
        and NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , con, p.mediana_con, 0.05 AS l_sup, 0 AS l_inf
        , sin_, p.mediana_sin, 1 AS l_sup, .98 AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY con) AS mediana_con, stddev_pop(con) AS desviacion_con
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY sin_) AS mediana_sin, stddev_pop(sin_) AS desviacion_sin
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'ALERTA_SIN_INFO': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN NUM_GRUPOHIT = 2 AND trim(des_mensajealerta) in ('NYYYN', 'NNNYN', 'NYNYN', 'NNYYN', 'NYYNY', 'NNYYY', 'NNNNN') THEN 1 ELSE 0 END)/count(*) AS gpo_7
        --, SUM(CASE WHEN NUM_GRUPOHIT = 2 AND trim(des_mensajealerta) in ('NNYNY') THEN 1 ELSE 0 END)/count(*) AS gpo_menos2
        --, SUM(CASE WHEN NUM_GRUPOHIT = 2 AND trim(des_mensajealerta) in ('NYNNN') THEN 1 ELSE 0 END)/count(*) AS gpo_menos15
        --, SUM(CASE WHEN NUM_GRUPOHIT = 2 AND trim(des_mensajealerta) in ('NNYNN', 'NYYNN', 'YNYNN') THEN 1 ELSE 0 END)/count(*) AS gpo_menos19
        , SUM(CASE WHEN NUM_GRUPOHIT = 2 AND trim(des_mensajealerta) NOT in ('NYYYN', 'NNNYN', 'NYNYN', 'NNYYN', 'NYYNY', 'NNYYY', 'NNNNN') THEN 1 ELSE 0 END)/count(*) AS otros
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        and NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN NUM_GRUPOHIT = 2 AND trim(des_mensajealerta) in ('NYYYN', 'NNNYN', 'NYNYN', 'NNYYN', 'NYYNY', 'NNYYY', 'NNNNN') THEN 1 ELSE 0 END)/count(*) AS gpo_7
        , SUM(CASE WHEN NUM_GRUPOHIT = 2 AND trim(des_mensajealerta) NOT in ('NYYYN', 'NNNYN', 'NYNYN', 'NNYYN', 'NYYNY', 'NNYYY', 'NNNNN') THEN 1 ELSE 0 END)/count(*) AS otros
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO > '20200815'
        and NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , gpo_7, p.mediana_7, p.mediana_7 + 2*p.desviacion_7 AS l_sup, p.mediana_7 - 2*p.desviacion_7 AS l_inf
        --, gpo_menos2, p.mediana_2, p.mediana_2 + 2*p.desviacion_2 AS l_sup, p.mediana_2 - 2*p.desviacion_2 AS l_inf
        --, gpo_menos15, p.mediana_15, p.mediana_15 + 2*p.desviacion_15 AS l_sup, p.mediana_15 - 2*p.desviacion_15 AS l_inf
        --, gpo_menos19, p.mediana_19, p.mediana_19 + 2*p.desviacion_19 AS l_sup, p.mediana_19 - 2*p.desviacion_19 AS l_inf
        , otros, p.mediana_o, p.mediana_o + 2*p.desviacion_o AS l_sup, p.mediana_o - 2*p.desviacion_o AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY gpo_7) AS mediana_7, stddev_pop(gpo_7) AS desviacion_7
        --, PERCENTILE_CONT(0.5) WITHIN group (ORDER BY gpo_menos2) AS mediana_2, stddev_pop(gpo_menos2) AS desviacion_2
        --, PERCENTILE_CONT(0.5) WITHIN group (ORDER BY gpo_menos15) AS mediana_15, stddev_pop(gpo_menos15) AS desviacion_15
        --, PERCENTILE_CONT(0.5) WITHIN group (ORDER BY gpo_menos19) AS mediana_19, stddev_pop(gpo_menos19) AS desviacion_19
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY otros) AS mediana_o, stddev_pop(otros) AS desviacion_o
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'ALERTA_CON_INFO': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN NUM_GRUPOHIT = 3 AND trim(des_mensajealerta) in ('NNNNN', 'NYNNN') THEN 1 ELSE 0 END)/count(*) AS gpo_1
        , SUM(CASE WHEN NUM_GRUPOHIT = 3 AND trim(des_mensajealerta) in ('NNNYN', 'NNYYN', 'NNYYY', 'NYNYN', 'NYYYN', 'NYYYY','NNYNY', 'NYYNY','YNNNN', 'YNYNN', 'YNYNY', 'YYNNN') THEN 1 ELSE 0 END)/count(*) AS gpo_27_2_12
        , SUM(CASE WHEN NUM_GRUPOHIT = 3 AND trim(des_mensajealerta) in ('NNYNN', 'NYYNN') THEN 1 ELSE 0 END)/count(*) AS gpo_menos12
        , SUM(CASE WHEN NUM_GRUPOHIT = 3 AND trim(des_mensajealerta) NOT in 
        ('NNNNN','NYNNN','NNNYN','NNYYN','NNYYY','NYNYN','NYYYN','NYYYY','NNYNN','NYYNN','NNYNY','NYYNY','YNNNN','YNYNN','YNYNY','YYNNN') THEN 1 ELSE 0 END)/count(*) AS otros
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        and NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN NUM_GRUPOHIT = 3 AND trim(des_mensajealerta) in ('NNNNN', 'NYNNN') THEN 1 ELSE 0 END)/count(*) AS gpo_1
        , SUM(CASE WHEN NUM_GRUPOHIT = 3 AND trim(des_mensajealerta) in ('NNNYN', 'NNYYN', 'NNYYY', 'NYNYN', 'NYYYN', 'NYYYY','NNYNY', 'NYYNY','YNNNN', 'YNYNN', 'YNYNY', 'YYNNN') THEN 1 ELSE 0 END)/count(*) AS gpo_27_2_12
        , SUM(CASE WHEN NUM_GRUPOHIT = 3 AND trim(des_mensajealerta) in ('NNYNN', 'NYYNN') THEN 1 ELSE 0 END)/count(*) AS gpo_menos12
        , SUM(CASE WHEN NUM_GRUPOHIT = 3 AND trim(des_mensajealerta) NOT in 
        ('NNNNN','NYNNN','NNNYN','NNYYN','NNYYY','NYNYN','NYYYN','NYYYY','NNYNN','NYYNN','NNYNY','NYYNY','YNNNN','YNYNN','YNYNY','YYNNN') THEN 1 ELSE 0 END)/count(*) AS otros
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO > '20200815'
        and NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , gpo_1, p.mediana_1, p.mediana_1 + p.desviacion_1 AS l_sup, p.mediana_1 - p.desviacion_1 AS l_inf
        , gpo_27_2_12, p.mediana_27_2_12, p.mediana_27_2_12 + 2*p.desviacion_27_2_12 AS l_sup, p.mediana_27_2_12 - 2*p.desviacion_27_2_12 AS l_inf
        , gpo_menos12, p.mediana_12, p.mediana_12 + 2*p.desviacion_12 AS l_sup, p.mediana_12 - 2*p.desviacion_12 AS l_inf
        , otros, p.mediana_o, p.mediana_o + 2*p.desviacion_o AS l_sup, p.mediana_o - 2*p.desviacion_o AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY gpo_1) AS mediana_1, stddev_pop(gpo_1) AS desviacion_1
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY gpo_27_2_12) AS mediana_27_2_12, stddev_pop(gpo_27_2_12) AS desviacion_27_2_12
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY gpo_menos12) AS mediana_12, stddev_pop(gpo_menos12) AS desviacion_12
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY otros) AS mediana_o, stddev_pop(otros) AS desviacion_o
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'PUESTOS': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN (num_opcionpuesto = 1 AND num_subopcionpuesto IN (1,2,3,6,7))
                                        OR (num_opcionpuesto = 2 AND num_subopcionpuesto BETWEEN 1 AND 6)
                                        OR (num_opcionpuesto = 5 AND num_subopcionpuesto IN (2,15,16))
                                        THEN 1 ELSE 0 END)/count(*) AS manual
        , SUM(CASE WHEN (num_opcionpuesto = 3 AND num_subopcionpuesto IN (1,4,5,6,7,8,9,10,11,12,13,15,
                                        18,19,20,21,22,23,24,25,26,27,28,30,31,33,34,35,40,41,42,43,44,46,47,48,49,52,53))
                                        OR (num_opcionpuesto = 5 AND num_subopcionpuesto IN (1,3,9,10,11,12,13,14,21))
                                        THEN 1 ELSE 0 END)/count(*) AS negocio
        , SUM(CASE WHEN (num_opcionpuesto = 6 AND num_subopcionpuesto = 99)
                                        OR (num_opcionpuesto = 7 AND num_subopcionpuesto = 99)
                                        OR (num_opcionpuesto = 8 AND num_subopcionpuesto = 99)
                                        OR (num_opcionpuesto = 9 AND num_subopcionpuesto = 99)
                                        OR (num_opcionpuesto = 10 AND num_subopcionpuesto = 99)
                                        THEN 1 ELSE 0 END)/count(*) AS no_trabaja
        , SUM(CASE WHEN (num_opcionpuesto = 1 AND num_subopcionpuesto IN (4,5,8))
                                        OR (num_opcionpuesto = 2 AND num_subopcionpuesto = 8)
                                        OR (num_opcionpuesto = 3 AND num_subopcionpuesto IN (2,3,29,37,51))
                                        OR (num_opcionpuesto = 5 AND num_subopcionpuesto IN (4,5,8,18,23))
                                        THEN 1 ELSE 0 END)/count(*) AS otros
        , SUM(CASE WHEN (num_opcionpuesto = 3 AND num_subopcionpuesto IN (14,16,17,36,38,39,50))
                                        OR (num_opcionpuesto = 4 AND num_subopcionpuesto IN (1,6))				
                                        OR (num_opcionpuesto = 5 AND num_subopcionpuesto IN (6,7,17,19,20))
                                        THEN 1 ELSE 0 END)/count(*) AS profesional				
        , SUM(CASE WHEN (num_opcionpuesto = 2 AND num_subopcionpuesto = 7)
                                        OR (num_opcionpuesto = 3 AND num_subopcionpuesto = 45)				
                                        OR (num_opcionpuesto = 5 AND num_subopcionpuesto = 22)
                                        OR (num_opcionpuesto = 4 AND num_subopcionpuesto IN (2,3,4,5,7))
                                        THEN 1 ELSE 0 END)/count(*) AS seguridad_transporte				

        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        and NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN (num_opcionpuesto = 1 AND num_subopcionpuesto IN (1,2,3,6,7))
                                        OR (num_opcionpuesto = 2 AND num_subopcionpuesto BETWEEN 1 AND 6)
                                        OR (num_opcionpuesto = 5 AND num_subopcionpuesto IN (2,15,16))
                                        THEN 1 ELSE 0 END)/count(*) AS manual
        , SUM(CASE WHEN (num_opcionpuesto = 3 AND num_subopcionpuesto IN (1,4,5,6,7,8,9,10,11,12,13,15,
                                        18,19,20,21,22,23,24,25,26,27,28,30,31,33,34,35,40,41,42,43,44,46,47,48,49,52,53))
                                        OR (num_opcionpuesto = 5 AND num_subopcionpuesto IN (1,3,9,10,11,12,13,14,21))
                                        THEN 1 ELSE 0 END)/count(*) AS negocio
        , SUM(CASE WHEN (num_opcionpuesto = 6 AND num_subopcionpuesto = 99)
                                        OR (num_opcionpuesto = 7 AND num_subopcionpuesto = 99)
                                        OR (num_opcionpuesto = 8 AND num_subopcionpuesto = 99)
                                        OR (num_opcionpuesto = 9 AND num_subopcionpuesto = 99)
                                        OR (num_opcionpuesto = 10 AND num_subopcionpuesto = 99)
                                        THEN 1 ELSE 0 END)/count(*) AS no_trabaja
        , SUM(CASE WHEN (num_opcionpuesto = 1 AND num_subopcionpuesto IN (4,5,8))
                                        OR (num_opcionpuesto = 2 AND num_subopcionpuesto = 8)
                                        OR (num_opcionpuesto = 3 AND num_subopcionpuesto IN (2,3,29,37,51))
                                        OR (num_opcionpuesto = 5 AND num_subopcionpuesto IN (4,5,8,18,23))
                                        THEN 1 ELSE 0 END)/count(*) AS otros
        , SUM(CASE WHEN (num_opcionpuesto = 3 AND num_subopcionpuesto IN (14,16,17,36,38,39,50))
                                        OR (num_opcionpuesto = 4 AND num_subopcionpuesto IN (1,6))				
                                        OR (num_opcionpuesto = 5 AND num_subopcionpuesto IN (6,7,17,19,20))
                                        THEN 1 ELSE 0 END)/count(*) AS profesional				
        , SUM(CASE WHEN (num_opcionpuesto = 2 AND num_subopcionpuesto = 7)
                                        OR (num_opcionpuesto = 3 AND num_subopcionpuesto = 45)				
                                        OR (num_opcionpuesto = 5 AND num_subopcionpuesto = 22)
                                        OR (num_opcionpuesto = 4 AND num_subopcionpuesto IN (2,3,4,5,7))
                                        THEN 1 ELSE 0 END)/count(*) AS seguridad_transporte		
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO > '20220126' AND FEC_MOVIMIENTO < '20220426'
        and NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , manual, p.mediana_manual, p.mediana_manual + 2*p.desviacion_manual AS l_sup, p.mediana_manual - 2*p.desviacion_manual AS l_inf
        , negocio, p.mediana_negocio, p.mediana_negocio + 2*p.desviacion_negocio AS l_sup, p.mediana_negocio - 2*p.desviacion_negocio AS l_inf
        , no_trabaja, p.mediana_no_trabaja, p.mediana_no_trabaja + 2*p.desviacion_no_trabaja AS l_sup, p.mediana_no_trabaja - 2*p.desviacion_no_trabaja AS l_inf
        , otros, p.mediana_otros, p.mediana_otros + 2*p.desviacion_otros AS l_sup, p.mediana_otros - 2*p.desviacion_otros AS l_inf
        , profesional, p.mediana_profesional, p.mediana_profesional + 2*p.desviacion_profesional AS l_sup, p.mediana_profesional - 2*p.desviacion_profesional AS l_inf
        , seguridad_transporte, p.mediana_seguridad, p.mediana_seguridad + 2*p.desviacion_seguridad AS l_sup, p.mediana_seguridad - 2*p.desviacion_seguridad AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY manual) AS mediana_manual, stddev_pop(manual) AS desviacion_manual
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY negocio) AS mediana_negocio, stddev_pop(negocio) AS desviacion_negocio
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY no_trabaja) AS mediana_no_trabaja, stddev_pop(no_trabaja) AS desviacion_no_trabaja
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY otros) AS mediana_otros, stddev_pop(otros) AS desviacion_otros
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY profesional) AS mediana_profesional, stddev_pop(profesional) AS desviacion_profesional
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY seguridad_transporte) AS mediana_seguridad, stddev_pop(seguridad_transporte) AS desviacion_seguridad
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'TIPO_PRODUCTO_MAX_PLAZO': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN trim(des_productomaximoplazo) = 'PL' 
                                        AND (num_maximoplazo >= 0 AND num_maximoplazo <= 273) 
                                        THEN 1 ELSE 0 END)/count(*) AS pp_273
        , SUM(CASE WHEN trim(des_productomaximoplazo) = 'PL' 
                                        AND (num_maximoplazo > 273 AND num_maximoplazo <= 390) 
                                        THEN 1 ELSE 0 END)/count(*) AS pp_273_390				
        , SUM(CASE WHEN trim(des_productomaximoplazo) = 'PL' 
                                        AND (num_maximoplazo > 390 AND num_maximoplazo <= 555) 
                                        THEN 1 ELSE 0 END)/count(*) AS pp_390_555
        , SUM(CASE WHEN trim(des_productomaximoplazo) = 'PL' 
                                        AND (num_maximoplazo > 555 AND num_maximoplazo <= 721) 
                                        THEN 1 ELSE 0 END)/count(*) AS pp_555_721
        , SUM(CASE WHEN trim(des_productomaximoplazo) = 'PL' 
                                        AND (num_maximoplazo > 721 AND num_maximoplazo <= 1435) 
                                        THEN 1 ELSE 0 END)/count(*) AS pp_721_1435
        , SUM(CASE WHEN trim(des_productomaximoplazo) = 'PL' 
                                        AND (num_maximoplazo > 1435) 
                                        THEN 1 ELSE 0 END)/count(*) AS pp_1435

        , SUM(CASE WHEN trim(des_productomaximoplazo) in ('CL','AF')
                                        AND (num_maximoplazo >= 0 AND num_maximoplazo <= 30) 
                                        THEN 1 ELSE 0 END)/count(*) AS lc_am_30	
        , SUM(CASE WHEN trim(des_productomaximoplazo) in ('CL','AF')
                                        AND (num_maximoplazo > 30 AND num_maximoplazo <= 555) 
                                        THEN 1 ELSE 0 END)/count(*) AS lc_am_30_555
        , SUM(CASE WHEN trim(des_productomaximoplazo) in ('CL','AF')
                                        AND (num_maximoplazo > 555) 
                                        THEN 1 ELSE 0 END)/count(*) AS lc_am_555
                                        
        , SUM(CASE WHEN trim(des_productomaximoplazo) in ('LS','PN')
                                        AND (num_maximoplazo >= 0) 
                                        THEN 1 ELSE 0 END)/count(*) AS a_pn

        , SUM(CASE WHEN trim(des_productomaximoplazo) in ('CT')
                                        AND (num_maximoplazo >= 0) 
                                        THEN 1 ELSE 0 END)/count(*) AS conColateral
                                        
        , SUM(CASE WHEN trim(des_productomaximoplazo) in ('AU')
                                        AND (num_maximoplazo >= 0) 
                                        THEN 1 ELSE 0 END)/count(*) AS compraAutomovil

        , SUM(CASE WHEN trim(des_productomaximoplazo) in ('MI')
                                        AND (num_maximoplazo >= 0) 
                                        THEN 1 ELSE 0 END)/count(*) AS otros				
                                        
        , SUM(CASE WHEN trim(des_productomaximoplazo) in ('RE')
                                        AND (num_maximoplazo >= 0) 
                                        THEN 1 ELSE 0 END)/count(*) AS bienesRaices
                                        
        , SUM(CASE WHEN trim(des_productomaximoplazo) NOT in ('','RE','MI','AU','CT','LS','PN','CL','AF','PL')
                                        AND (num_maximoplazo >= 0) 
                                        THEN 1 ELSE 0 END)/count(*) AS cualquierOtro
                                        
        , SUM(CASE WHEN trim(des_productomaximoplazo) = ''
                                        OR (num_maximoplazo < 0) 
                                        THEN 1 ELSE 0 END)/count(*) AS na
                                        
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        and NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN trim(des_productomaximoplazo) = 'PL' 
                                        AND (num_maximoplazo >= 0 AND num_maximoplazo <= 273) 
                                        THEN 1 ELSE 0 END)/count(*) AS pp_273
        , SUM(CASE WHEN trim(des_productomaximoplazo) = 'PL' 
                                        AND (num_maximoplazo > 273 AND num_maximoplazo <= 390) 
                                        THEN 1 ELSE 0 END)/count(*) AS pp_273_390				
        , SUM(CASE WHEN trim(des_productomaximoplazo) = 'PL' 
                                        AND (num_maximoplazo > 390 AND num_maximoplazo <= 555) 
                                        THEN 1 ELSE 0 END)/count(*) AS pp_390_555
        , SUM(CASE WHEN trim(des_productomaximoplazo) = 'PL' 
                                        AND (num_maximoplazo > 555 AND num_maximoplazo <= 721) 
                                        THEN 1 ELSE 0 END)/count(*) AS pp_555_721
        , SUM(CASE WHEN trim(des_productomaximoplazo) = 'PL' 
                                        AND (num_maximoplazo > 721 AND num_maximoplazo <= 1435) 
                                        THEN 1 ELSE 0 END)/count(*) AS pp_721_1435
        , SUM(CASE WHEN trim(des_productomaximoplazo) = 'PL' 
                                        AND (num_maximoplazo > 1435) 
                                        THEN 1 ELSE 0 END)/count(*) AS pp_1435

        , SUM(CASE WHEN trim(des_productomaximoplazo) in ('CL','AF')
                                        AND (num_maximoplazo >= 0 AND num_maximoplazo <= 30) 
                                        THEN 1 ELSE 0 END)/count(*) AS lc_am_30	
        , SUM(CASE WHEN trim(des_productomaximoplazo) in ('CL','AF')
                                        AND (num_maximoplazo > 30 AND num_maximoplazo <= 555) 
                                        THEN 1 ELSE 0 END)/count(*) AS lc_am_30_555
        , SUM(CASE WHEN trim(des_productomaximoplazo) in ('CL','AF')
                                        AND (num_maximoplazo > 555) 
                                        THEN 1 ELSE 0 END)/count(*) AS lc_am_555
                                        
        , SUM(CASE WHEN trim(des_productomaximoplazo) in ('LS','PN')
                                        AND (num_maximoplazo >= 0) 
                                        THEN 1 ELSE 0 END)/count(*) AS a_pn

        , SUM(CASE WHEN trim(des_productomaximoplazo) in ('CT')
                                        AND (num_maximoplazo >= 0) 
                                        THEN 1 ELSE 0 END)/count(*) AS conColateral
                                        
        , SUM(CASE WHEN trim(des_productomaximoplazo) in ('AU')
                                        AND (num_maximoplazo >= 0) 
                                        THEN 1 ELSE 0 END)/count(*) AS compraAutomovil

        , SUM(CASE WHEN trim(des_productomaximoplazo) in ('MI')
                                        AND (num_maximoplazo >= 0) 
                                        THEN 1 ELSE 0 END)/count(*) AS otros				
                                        
        , SUM(CASE WHEN trim(des_productomaximoplazo) in ('RE')
                                        AND (num_maximoplazo >= 0) 
                                        THEN 1 ELSE 0 END)/count(*) AS bienesRaices
                                        
        , SUM(CASE WHEN trim(des_productomaximoplazo) NOT in ('','RE','MI','AU','CT','LS','PN','CL','AF','PL')
                                        AND (num_maximoplazo >= 0) 
                                        THEN 1 ELSE 0 END)/count(*) AS cualquierOtro
                                        
        , SUM(CASE WHEN trim(des_productomaximoplazo) = ''
                                        OR (num_maximoplazo < 0) 
                                        THEN 1 ELSE 0 END)/count(*) AS na
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO > '20210830' AND FEC_MOVIMIENTO < '20211006'
        and NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , pp_273, p.mediana_pp_273, p.mediana_pp_273 + 3*p.desviacion_pp_273 AS l_sup, p.mediana_pp_273 - 3*p.desviacion_pp_273 AS l_inf
        , pp_273_390, p.mediana_pp_273_390, p.mediana_pp_273_390 + 3*p.desviacion_pp_273_390 AS l_sup, p.mediana_pp_273_390 - 3*p.desviacion_pp_273_390 AS l_inf
        , pp_390_555, p.mediana_pp_390_555, p.mediana_pp_390_555 + 3*p.desviacion_pp_390_555 AS l_sup, p.mediana_pp_390_555 - 3*p.desviacion_pp_390_555 AS l_inf
        , pp_555_721, p.mediana_pp_555_721, p.mediana_pp_555_721 + 3*p.desviacion_pp_555_721 AS l_sup, p.mediana_pp_555_721 - 3*p.desviacion_pp_555_721 AS l_inf
        , pp_721_1435, p.mediana_pp_721_1435, p.mediana_pp_721_1435 + 3*p.desviacion_pp_721_1435 AS l_sup, p.mediana_pp_721_1435 - 3*p.desviacion_pp_721_1435 AS l_inf
        , pp_1435, p.mediana_pp_1435, p.mediana_pp_1435 + 3*p.desviacion_pp_1435 AS l_sup, p.mediana_pp_1435 - 3*p.desviacion_pp_1435 AS l_inf
        , lc_am_30, p.mediana_lc_am_30, p.mediana_lc_am_30 + 3*p.desviacion_lc_am_30 AS l_sup, p.mediana_lc_am_30 - 3*p.desviacion_lc_am_30 AS l_inf
        , lc_am_30_555, p.mediana_lc_am_30_555, p.mediana_lc_am_30_555 + 3*p.desviacion_lc_am_30_555 AS l_sup, p.mediana_lc_am_30_555 - 3*p.desviacion_lc_am_30_555 AS l_inf
        , lc_am_555, p.mediana_lc_am_555, p.mediana_lc_am_555 + 3*p.desviacion_lc_am_555 AS l_sup, p.mediana_lc_am_555 - 3*p.desviacion_lc_am_555 AS l_inf
        , a_pn, p.mediana_a_pn, p.mediana_a_pn + 3*p.desviacion_a_pn AS l_sup, p.mediana_a_pn - 3*p.desviacion_a_pn AS l_inf
        , conColateral, p.mediana_conColateral, p.mediana_conColateral + 3*p.desviacion_conColateral AS l_sup, p.mediana_conColateral - 3*p.desviacion_conColateral AS l_inf
        , compraAutomovil, p.mediana_compraAutomovil, p.mediana_compraAutomovil + 3*p.desviacion_compraAutomovil AS l_sup, p.mediana_compraAutomovil - 3*p.desviacion_compraAutomovil AS l_inf
        , otros, p.mediana_otros, p.mediana_otros + 3*p.desviacion_otros AS l_sup, p.mediana_otros - 3*p.desviacion_otros AS l_inf
        , bienesRaices, p.mediana_bienesRaices, p.mediana_bienesRaices + 3*p.desviacion_bienesRaices AS l_sup, p.mediana_bienesRaices - 3*p.desviacion_bienesRaices AS l_inf
        , cualquierOtro, p.mediana_cualquierOtro, p.mediana_cualquierOtro + 3*p.desviacion_cualquierOtro AS l_sup, p.mediana_cualquierOtro - 3*p.desviacion_cualquierOtro AS l_inf
        , na, p.mediana_na, p.mediana_na + 3*p.desviacion_na AS l_sup, p.mediana_na - 3*p.desviacion_na AS l_inf

        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY pp_273) AS mediana_pp_273, stddev_pop(pp_273) AS desviacion_pp_273
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY pp_273_390) AS mediana_pp_273_390, stddev_pop(pp_273_390) AS desviacion_pp_273_390
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY pp_390_555) AS mediana_pp_390_555, stddev_pop(pp_390_555) AS desviacion_pp_390_555
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY pp_555_721) AS mediana_pp_555_721, stddev_pop(pp_555_721) AS desviacion_pp_555_721
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY pp_721_1435) AS mediana_pp_721_1435, stddev_pop(pp_721_1435) AS desviacion_pp_721_1435
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY pp_1435) AS mediana_pp_1435, stddev_pop(pp_1435) AS desviacion_pp_1435
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY lc_am_30) AS mediana_lc_am_30, stddev_pop(lc_am_30) AS desviacion_lc_am_30
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY lc_am_30_555) AS mediana_lc_am_30_555, stddev_pop(lc_am_30_555) AS desviacion_lc_am_30_555
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY lc_am_555) AS mediana_lc_am_555, stddev_pop(lc_am_555) AS desviacion_lc_am_555
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY a_pn) AS mediana_a_pn, stddev_pop(a_pn) AS desviacion_a_pn
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY conColateral) AS mediana_conColateral, stddev_pop(conColateral) AS desviacion_conColateral
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY compraAutomovil) AS mediana_compraAutomovil, stddev_pop(compraAutomovil) AS desviacion_compraAutomovil
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY otros) AS mediana_otros, stddev_pop(otros) AS desviacion_otros
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY bienesRaices) AS mediana_bienesRaices, stddev_pop(bienesRaices) AS desviacion_bienesRaices
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY cualquierOtro) AS mediana_cualquierOtro, stddev_pop(cualquierOtro) AS desviacion_cualquierOtro
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY na) AS mediana_na, stddev_pop(na) AS desviacion_na
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'ESTATUS_COPPEL': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_ESTATUSSOLICITUD = 'A' THEN 1 ELSE 0 END)/count(*) AS autorizadas
        , SUM(CASE WHEN CLV_ESTATUSSOLICITUD = 'R' THEN 1 ELSE 0 END)/count(*) AS rechazadas
        , SUM(CASE WHEN CLV_ESTATUSSOLICITUD = 'S' THEN 1 ELSE 0 END)/count(*) AS orden_supervision
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_ESTATUSSOLICITUD = 'A' THEN 1 ELSE 0 END)/count(*) AS autorizadas
        , SUM(CASE WHEN CLV_ESTATUSSOLICITUD = 'R' THEN 1 ELSE 0 END)/count(*) AS rechazadas
        , SUM(CASE WHEN CLV_ESTATUSSOLICITUD = 'S' THEN 1 ELSE 0 END)/count(*) AS orden_supervision
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= '20211104' AND FEC_MOVIMIENTO <= '20220430'
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , AUTORIZADAS, p.mediana_a, p.mediana_a + 3*p.desviacion_a AS l_sup, p.mediana_a - 3*p.desviacion_a AS l_inf
        , RECHAZADAS, p.mediana_r, p.mediana_r + 3*p.desviacion_r AS l_sup, p.mediana_r - 3*p.desviacion_r AS l_inf
        , ORDEN_SUPERVISION, p.mediana_os, p.mediana_os + 3*p.desviacion_os AS l_sup, p.mediana_os - 3*p.desviacion_os AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY AUTORIZADAS ) AS mediana_a, stddev_pop(AUTORIZADAS ) AS desviacion_a
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY RECHAZADAS ) AS mediana_r, stddev_pop(RECHAZADAS ) AS desviacion_r
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY ORDEN_SUPERVISION ) AS mediana_os, stddev_pop(ORDEN_SUPERVISION ) AS desviacion_os
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'LIMITE_CREDITO_PESOS': """
        select * from ( WITH tmp AS 
        (SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , avg(NUM_LIMITECREDITOPESOS) AS NUM_LIMITECREDITOPESOS
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000 AND CLV_ESTATUSSOLICITUD IN ('A','S')
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 as
        (SELECT date(FEC_MOVIMIENTO) AS fecha
        , avg(NUM_LIMITECREDITOPESOS) AS NUM_LIMITECREDITOPESOS
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO > '20210216' and  FEC_MOVIMIENTO < '20210530'
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000 AND CLV_ESTATUSSOLICITUD IN ('A','S')
        GROUP BY 1
        ORDER BY 1)
        SELECT tmp.fecha
        , tmp.NUM_LIMITECREDITOPESOS, avg(tmp2.NUM_LIMITECREDITOPESOS) AS media, avg(tmp2.NUM_LIMITECREDITOPESOS) + 3*stddev_pop(tmp2.NUM_LIMITECREDITOPESOS) AS l_sup, avg(tmp2.NUM_LIMITECREDITOPESOS) - 3*stddev_pop(tmp2.NUM_LIMITECREDITOPESOS) AS l_inf
        FROM tmp, tmp2
        GROUP BY 1,2
        ORDER BY fecha) a order by 1
        """,
'TELEFONOS_INVALIDOS_COMPLETO': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_TIPOTELEFONO = 0 THEN 1 ELSE 0 END)/count(*) AS invalido
        , SUM(CASE WHEN CLV_TIPOTELEFONO = 1 THEN 1 ELSE 0 END)/count(*) AS casa_valido
        , SUM(CASE WHEN CLV_TIPOTELEFONO = 2 THEN 1 ELSE 0 END)/count(*) AS celular_valido
        , SUM(CASE WHEN CLV_TIPOTELEFONO = 3 THEN 1 ELSE 0 END)/count(*) AS casa_celular_valido
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_TIPOTELEFONO = 0 THEN 1 ELSE 0 END)/count(*) AS invalido
        , SUM(CASE WHEN CLV_TIPOTELEFONO = 1 THEN 1 ELSE 0 END)/count(*) AS casa_valido
        , SUM(CASE WHEN CLV_TIPOTELEFONO = 2 THEN 1 ELSE 0 END)/count(*) AS celular_valido
        , SUM(CASE WHEN CLV_TIPOTELEFONO = 3 THEN 1 ELSE 0 END)/count(*) AS casa_celular_valido
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= '20220126' AND FEC_MOVIMIENTO <= '20220326'
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , INVALIDO, p.mediana1, p.mediana1 + 2*p.desviacion1 AS l_sup, (CASE WHEN (p.mediana1 - 2*p.desviacion1 < 0) then 0 else (p.mediana1 - 2*p.desviacion1) END) AS l_inf
        , CASA_VALIDO, p.mediana2, p.mediana2 + 2*p.desviacion2 AS l_sup, (CASE WHEN (p.mediana2 - 2*p.desviacion2 < 0) then 0 else (p.mediana2 - 2*p.desviacion2) END) AS l_inf
        , CELULAR_VALIDO, p.mediana3, p.mediana3 + 2*p.desviacion3 AS l_sup, (CASE WHEN (p.mediana3 - 2*p.desviacion3 < 0) then 0 else (p.mediana3 - 2*p.desviacion3) END) AS l_inf
        , CASA_CELULAR_VALIDO, p.mediana4, p.mediana4 + 2*p.desviacion4 AS l_sup, (CASE WHEN (p.mediana4 - 2*p.desviacion4 < 0) then 0 else (p.mediana4 - 2*p.desviacion4) END) AS l_inf
        FROM tmp, 
        (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY INVALIDO) AS mediana1, stddev_pop(invalido) AS desviacion1
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY CASA_VALIDO) AS mediana2, stddev_pop(CASA_VALIDO) AS desviacion2
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY CELULAR_VALIDO) AS mediana3, stddev_pop(CELULAR_VALIDO) AS desviacion3
        ,PERCENTILE_CONT(0.5) WITHIN group (ORDER BY CASA_CELULAR_VALIDO) AS mediana4, stddev_pop(CASA_CELULAR_VALIDO) AS desviacion4
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'GRUPO_EVALUACION_CON_5': """
    select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN NUM_GRUPOEVALUACION = 1 THEN 1 ELSE 0 END)/count(*) AS uno
        , SUM(CASE WHEN NUM_GRUPOEVALUACION = 2 THEN 1 ELSE 0 END)/count(*) AS dos
        , SUM(CASE WHEN NUM_GRUPOEVALUACION = 3 THEN 1 ELSE 0 END)/count(*) AS tres
        , SUM(CASE WHEN NUM_GRUPOEVALUACION = 4 THEN 1 ELSE 0 END)/count(*) AS cuatro
        , SUM(CASE WHEN NUM_GRUPOEVALUACION = 5 THEN 1 ELSE 0 END)/count(*) AS cinco
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN NUM_GRUPOEVALUACION = 1 THEN 1 ELSE 0 END)/count(*) AS uno
        , SUM(CASE WHEN NUM_GRUPOEVALUACION = 2 THEN 1 ELSE 0 END)/count(*) AS dos
        , SUM(CASE WHEN NUM_GRUPOEVALUACION = 3 THEN 1 ELSE 0 END)/count(*) AS tres
        , SUM(CASE WHEN NUM_GRUPOEVALUACION = 4 THEN 1 ELSE 0 END)/count(*) AS cuatro
        , SUM(CASE WHEN NUM_GRUPOEVALUACION = 5 THEN 1 ELSE 0 END)/count(*) AS cinco
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= '20211109' and FEC_MOVIMIENTO < '20211220'
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , uno, p.mediana_1, (CASE WHEN (p.mediana_1 + 3*p.desviacion_1 > 1) then 1 else (p.mediana_1 + 3*p.desviacion_1) END) AS l_sup, (CASE WHEN (p.mediana_1 - 3*p.desviacion_1 < 0) then 0 else (p.mediana_1 - 3*p.desviacion_1) END) AS l_inf
        , dos, p.mediana_2, (CASE WHEN (p.mediana_2 + 3*p.desviacion_2 > 1) then 1 else (p.mediana_2 + 3*p.desviacion_2) END) AS l_sup, (CASE WHEN (p.mediana_2 - 3*p.desviacion_2 < 0) then 0 else (p.mediana_2 - 3*p.desviacion_2) END) AS l_inf
        , tres, p.mediana_3, (CASE WHEN (p.mediana_3 + 3*p.desviacion_3 > 1) then 1 else (p.mediana_3 + 3*p.desviacion_3) END) AS l_sup, (CASE WHEN (p.mediana_3 - 3*p.desviacion_3 < 0) then 0 else (p.mediana_3 - 3*p.desviacion_3) END) AS l_inf
        , cuatro, p.mediana_4, (CASE WHEN (p.mediana_4 + 3*p.desviacion_4 > 1) then 1 else (p.mediana_4 + 3*p.desviacion_4) END) AS l_sup, (CASE WHEN (p.mediana_4 - 3*p.desviacion_4 < 0) then 0 else (p.mediana_4 - 3*p.desviacion_4) END) AS l_inf
        , cinco, p.mediana_5, (CASE WHEN (p.mediana_5 + 3*p.desviacion_5 > 1) then 1 else (p.mediana_5 + 3*p.desviacion_5) END) AS l_sup, (CASE WHEN (p.mediana_5 - 3*p.desviacion_5 < 0) then 0 else (p.mediana_5 - 3*p.desviacion_5) END) AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY uno) AS mediana_1, stddev_pop(uno) AS desviacion_1
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY dos) AS mediana_2, stddev_pop(dos) AS desviacion_2
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY tres) AS mediana_3, stddev_pop(tres) AS desviacion_3
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY cuatro) AS mediana_4, stddev_pop(cuatro) AS desviacion_4
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY cinco) AS mediana_5, stddev_pop(cinco) AS desviacion_5
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'TIPO_CREDITO': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN NUM_FLAGLINEACREDITOESPECIAL = 0 THEN 1 ELSE 0 END)/count(*) AS normal
        , SUM(CASE WHEN NUM_FLAGLINEACREDITOESPECIAL = 1 THEN 1 ELSE 0 END)/count(*) AS especial
        , SUM(CASE WHEN NUM_FLAGLINEACREDITOESPECIAL = 2 THEN 1 ELSE 0 END)/count(*) AS inicial     
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN NUM_FLAGLINEACREDITOESPECIAL = 0 THEN 1 ELSE 0 END)/count(*) AS normal
        , SUM(CASE WHEN NUM_FLAGLINEACREDITOESPECIAL = 1 THEN 1 ELSE 0 END)/count(*) AS especial
        , SUM(CASE WHEN NUM_FLAGLINEACREDITOESPECIAL = 2 THEN 1 ELSE 0 END)/count(*) AS inicial
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= '20211105' AND FEC_MOVIMIENTO < '20211220'
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , normal, p.mediana_1, (CASE WHEN (p.mediana_1 + 3*p.desviacion_1 > 1) then 1 else (p.mediana_1 + 3*p.desviacion_1) END) AS l_sup, (CASE WHEN (p.mediana_1 - 3*p.desviacion_1 < 0) then 0 else (p.mediana_1 - 3*p.desviacion_1) END) AS l_inf
        , especial, p.mediana_2, (CASE WHEN (p.mediana_2 + 3*p.desviacion_2 > 1) then 1 else (p.mediana_2 + 3*p.desviacion_2) END) AS l_sup, (CASE WHEN (p.mediana_2 - 3*p.desviacion_2 < 0) then 0 else (p.mediana_2 - 3*p.desviacion_2) END) AS l_inf
        , inicial, p.mediana_3, (CASE WHEN (p.mediana_3 + 3*p.desviacion_3 > 1) then 1 else (p.mediana_3 + 3*p.desviacion_3) END) AS l_sup, (CASE WHEN (p.mediana_3 - 3*p.desviacion_3 < 0) then 0 else (p.mediana_3 - 3*p.desviacion_3) END) AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY normal) AS mediana_1, stddev_pop(normal) AS desviacion_1
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY especial) AS mediana_2, stddev_pop(especial) AS desviacion_2
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY inicial) AS mediana_3, stddev_pop(inicial) AS desviacion_3
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'RESCATADOS_BURO': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_CLIENTERESCATEBURO = 0 THEN 1 ELSE 0 END)/count(*) AS no_rescatado
        , SUM(CASE WHEN CLV_CLIENTERESCATEBURO = 1 THEN 1 ELSE 0 END)/count(*) AS rescatado
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_CLIENTERESCATEBURO = 0 THEN 1 ELSE 0 END)/count(*) AS no_rescatado
        , SUM(CASE WHEN CLV_CLIENTERESCATEBURO = 1 THEN 1 ELSE 0 END)/count(*) AS rescatado
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= '20210901' AND FEC_MOVIMIENTO < '20211231'
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , no_rescatado, p.mediana_1, (CASE WHEN (p.mediana_1 + 2*p.desviacion_1 > 1) then 1 else (p.mediana_1 + 2*p.desviacion_1) END) AS l_sup, (CASE WHEN (p.mediana_1 - 2*p.desviacion_1 < 0) then 0 else (p.mediana_1 - 2*p.desviacion_1) END) AS l_inf
        , rescatado, p.mediana_2, (CASE WHEN (p.mediana_2 + 2*p.desviacion_2 > 1) then 1 else (p.mediana_2 + 2*p.desviacion_2) END) AS l_sup, (CASE WHEN (p.mediana_2 - 2*p.desviacion_2 < 0) then 0 else (p.mediana_2 - 2*p.desviacion_2) END) AS l_inf        
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY no_rescatado) AS mediana_1, stddev_pop(no_rescatado) AS desviacion_1
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY rescatado) AS mediana_2, stddev_pop(rescatado) AS desviacion_2
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'MODALIDAD_SOLICITUD': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN NUM_MODALIDADSOLICITUD = 0 THEN 1 ELSE 0 END)/count(*) AS automatica
        , SUM(CASE WHEN NUM_MODALIDADSOLICITUD = 1 THEN 1 ELSE 0 END)/count(*) AS normal
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN NUM_MODALIDADSOLICITUD = 0 THEN 1 ELSE 0 END)/count(*) AS automatica
        , SUM(CASE WHEN NUM_MODALIDADSOLICITUD = 1 THEN 1 ELSE 0 END)/count(*) AS normal
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= '20210101' AND FEC_MOVIMIENTO < '20211109'
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , automatica, p.mediana_1, (CASE WHEN (p.mediana_1 + 3*p.desviacion_1 > 1) then 1 else (p.mediana_1 + 3*p.desviacion_1) END) AS l_sup, (CASE WHEN (p.mediana_1 - 3*p.desviacion_1 < 0) then 0 else (p.mediana_1 - 3*p.desviacion_1) END) AS l_inf
        , normal, p.mediana_2, (CASE WHEN (p.mediana_2 + 3*p.desviacion_2 > 1) then 1 else (p.mediana_2 + 3*p.desviacion_2) END) AS l_sup, (CASE WHEN (p.mediana_2 - 3*p.desviacion_2 < 0) then 0 else (p.mediana_2 - 3*p.desviacion_2) END) AS l_inf        
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY automatica) AS mediana_1, stddev_pop(automatica) AS desviacion_1
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY normal) AS mediana_2, stddev_pop(normal) AS desviacion_2
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """,
'PRODUCTO_COPPEL': """
        select * from ( WITH tmp as (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_PRODUCTOCOPPEL = '1' THEN 1 ELSE 0 END)/count(*) AS coppel
        , SUM(CASE WHEN CLV_PRODUCTOCOPPEL = '2' THEN 1 ELSE 0 END)/count(*) AS motos
        , SUM(CASE WHEN CLV_PRODUCTOCOPPEL = '3' THEN 1 ELSE 0 END)/count(*) AS ambos
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= CURRENT_DATE - 90
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        ORDER BY fecha),
        tmp2 AS (
        SELECT DATE(FEC_MOVIMIENTO) AS fecha
        , EXTRACT(DAY FROM FEC_MOVIMIENTO) AS dia
        , SUM(CASE WHEN CLV_PRODUCTOCOPPEL = '1' THEN 1 ELSE 0 END)/count(*) AS coppel
        , SUM(CASE WHEN CLV_PRODUCTOCOPPEL = '2' THEN 1 ELSE 0 END)/count(*) AS motos
        , SUM(CASE WHEN CLV_PRODUCTOCOPPEL = '3' THEN 1 ELSE 0 END)/count(*) AS ambos
        FROM CALIDAD.ADMIN.MOV_PARAMETRICOCERTIFICACIONES
        WHERE FEC_MOVIMIENTO >= '20211109' AND FEC_MOVIMIENTO < '20211209'
        AND NUM_SOLICITUD > 650000000000 AND NUM_SOLICITUD < 850000000000
        GROUP BY fecha, dia
        )
        SELECT fecha
        , coppel, p.mediana_1, (CASE WHEN (p.mediana_1 + 3*p.desviacion_1 > 1) then 1 else (p.mediana_1 + 3*p.desviacion_1) END) AS l_sup, (CASE WHEN (p.mediana_1 - 3*p.desviacion_1 < 0) then 0 else (p.mediana_1 - 3*p.desviacion_1) END) AS l_inf
        , motos, p.mediana_2, (CASE WHEN (p.mediana_2 + 3*p.desviacion_2 > 1) then 1 else (p.mediana_2 + 3*p.desviacion_2) END) AS l_sup, (CASE WHEN (p.mediana_2 - 3*p.desviacion_2 < 0) then 0 else (p.mediana_2 - 3*p.desviacion_2) END) AS l_inf
        , ambos, p.mediana_3, (CASE WHEN (p.mediana_3 + 3*p.desviacion_3 > 1) then 1 else (p.mediana_3 + 3*p.desviacion_3) END) AS l_sup, (CASE WHEN (p.mediana_3 - 3*p.desviacion_3 < 0) then 0 else (p.mediana_3 - 3*p.desviacion_3) END) AS l_inf
        FROM tmp, (SELECT 
        PERCENTILE_CONT(0.5) WITHIN group (ORDER BY coppel) AS mediana_1, stddev_pop(coppel) AS desviacion_1
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY motos) AS mediana_2, stddev_pop(motos) AS desviacion_2
        , PERCENTILE_CONT(0.5) WITHIN group (ORDER BY ambos) AS mediana_3, stddev_pop(ambos) AS desviacion_3
        FROM tmp2) p
        ORDER BY fecha) a order by 1
        """
}