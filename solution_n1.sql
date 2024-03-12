------Solución prueba técnica Arcoprime, Item 1-----------

--Supuestos Pregunta N°1.1:
-----El código se creó tomando en cuenta que se ejecutará en Bigquery
-----Dado que en la tabla "hijos" no aparece el ID de la madre, se asocia el hijo al matrimonio siempre y cuando la madre estuviera viva durante su nacimiento.
-----Un padre puede haberse casado muchas veces, por lo que el hijo se asocia al matrimonio más cercano anterior a su nacimiento.
-----Se va a considerar que un hijo pudo haber nacido el mismo día del matrimonio.
-----Se va a considerar que un hijo pudo haber nacido y ese mismo día la madre hubiese fallecido.
-----Varios de estos supuestos se evitarían si en la tabla "hijos" existiera una columna con el "id de la madre"
-----La base de datos maneja el uso de la función de ventana ROW_NUMBER() OVER() y la condición QUALIFY.
-----Como no se indica la cantidad de decimales, se procede a redondear al primer decimal.
-----Se asume que en la tabla "conyuges" el "id_persona_1" corresponde al Padre y el "id_persona_2" a la madre.

--Tabla auxiliar para obtener los distintos hijos por matrimonio
WITH hijos_en_matrimonio AS (
  SELECT cys.id 
        ,cys.id_persona_1 AS padre
        ,cys.id_persona_2 AS madre
        ,cys.celebracion
        ,hjs.id_hijo
        ,prs_1.nacimiento
        ,ROW_NUMBER() OVER (PARTITION BY cys.id_persona_1, hjs.id_hijo ORDER BY cys.celebracion DESC) AS rn_celebracion
  FROM conyuges AS cys
  INNER JOIN hijos AS hjs ON hjs.id_padre=cys.id_persona_1
  INNER JOIN personas AS prs_1 ON prs_1.id=hjs.id_hijo AND prs_1.nacimiento>=cys.celebracion
  INNER JOIN personas AS prs_2 ON prs_2.defuncion>=prs_1.nacimiento
  QUALIFY rn_celebracion=1
),

--Respuesta 1.1: Promedio de hijos por matrimonio
q_promedio_hijos_matrimonio AS (
  SELECT ROUND(AVG(q_hijos),1) AS q_promedio_hijos_x_matrimonio
  FROM (
        SELECT id, count(*) AS q_hijos
        FROM hijos_en_matrimonio
        GROUP BY id
  )
),


--Supuestos Pregunta N°1.2:
-----El código se creó tomando en cuenta que se ejecutará en Bigquery.
-----Dado que la pregunta no hace alusión al matrimonio, no se usará la tabla "conyuges".
-----Un padre puede tener varios hijos.
-----La base de datos maneja el uso de la función de ventana ROW_NUMBER() OVER() y la condición QUALIFY.
-----Dado que no se especifica que sean personas vivas o muertas, se consideran ambos.

--Tabla Auxiliar para saber la cantidad de hijos que tiene cada padre
padres_con_hijos AS (
  SELECT id_padre, count(*) AS q_hijos
  FROM hijos
  GROUP BY id_padre
),

--Tabla Auxiliar para saber la cantidad de nietos que tiene cada abuelo
abuelos_con_nietos AS (
  SELECT hjs.id_padre, COUNT(*) AS q_nietos
  FROM hijos AS hjs
  INNER JOIN padres_con_hijos AS pds_hjs ON pds_hjs.id_padre=hjs.id_hijo
  GROUP BY hjs.id_padre
),

--Respuesta 1.2: Persona con mayor cantidad de nietos
max_abuelo_con_nietos AS (
  SELECT max_abuelo.id
        ,max_abuelo.q_nietos
        ,prs.nombre
        ,prs.rut
        ,prs.dv
        ,prs.nacimiento
        ,prs.defuncion
  FROM ( 
        SELECT id_padre AS id
              ,q_nietos
              ,ROW_NUMBER() OVER(ORDER BY q_nietos DESC) AS rn_q_nietos
        FROM abuelos_con_nietos AS abs_nts
        QUALIFY rn_q_nietos=1
  ) AS max_abuelo
  INNER JOIN personas AS prs USING(id)
)

SELECT *
FROM q_promedio_hijos_matrimonio --max_abuelo_con_nietos , aquí se escoge la métrica que se desea
