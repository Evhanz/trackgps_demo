
======= Funciones ===== 
CREATE OR REPLACE FUNCTION public.process_historic_data_tracking()
 RETURNS void
 LANGUAGE plpgsql
AS $function$
DECLARE
  oldTruckRow          ta_datacamion%ROWTYPE;
  historicTruckRow     ta_datacamion_historic%ROWTYPE;
  oldShovelRow         ta_datapala%ROWTYPE;
  historicShovelRow    ta_datapala_historic%ROWTYPE;
  oldAuxiliaryRow      ta_data_auxiliares%ROWTYPE;
  historicAuxiliaryRow ta_data_auxiliares_historic%ROWTYPE;
  startTime            TIMESTAMP;
  insertedRecords      INTEGER := 0;
  updatedRecords       INTEGER := 0;
    applicationTime TIMESTAMP ;
BEGIN

  startTime := clock_timestamp();
  applicationTime := DATE_TRUNC('HOUR', NOW() - interval '2 hours');
  FOR oldTruckRow IN SELECT * FROM ta_datacamion as da WHERE tiem_creac < applicationTime 
  					and (select count(id) from ta_datacamion where tiem_creac > da.tiem_creac and id_equipo = da.id_equipo ) > 2
  					and id_equipo in (
					select  id_equipo from ts_equipos te 
					where outside_tracking = true 
					and tiem_elimin is null)
    LOOP
      RAISE NOTICE 'Truck Inserting %', oldTruckRow.id;

      SELECT * INTO historicTruckRow
      FROM ta_datacamion_historic
      WHERE id_equipo = oldTruckRow.id_equipo
        AND tiem_creac = oldTruckRow.tiem_creac;

      IF (historicTruckRow.id IS NULL)
      THEN
        insertedRecords := insertedRecords + 1;
        INSERT INTO public.ta_datacamion_historic (id,
                               id_equipo,
                               frecuencia,
                               id_trabajador,
                               senhalgps,
                               senhalwireless,
                               calidadwireless,
                               tempeje1,
                               tempeje2,
                               tempeje3,
                               tempeje4,
                               tempeje5,
                               tempeje6,
                               presllanta1,
                               presllanta2,
                               presllanta3,
                               presllanta4,
                               presllanta5,
                               presllanta6,
                               velocidad,
                               isload,
                               tonelaje,
                               marcha,
                               incl_roll,
                               incl_pitch,
                               latitude,
                               longitud,
                               xcoor,
                               ycoor,
                               zcoor,
                               precisiongps,
                               tramosids,
                               direccion,
                               combustibleint,
                               templlanta1,
                               templlanta2,
                               templlanta3,
                               templlanta4,
                               templlanta5,
                               templlanta6,
                               bateriasensorllanta1,
                               bateriasensorllanta2,
                               bateriasensorllanta3,
                               bateriasensorllanta4,
                               bateriasensorllanta5,
                               bateriasensorllanta6,
                               tiem_creac,
                               tiem_update,
                               segment_angle)
        VALUES (((SELECT (coalesce(max(id), 0)) + 1 FROM public.ta_datacamion_historic)),
            oldTruckRow.id_equipo,
            oldTruckRow.frecuencia,
            oldTruckRow.id_trabajador,
            oldTruckRow.senhalgps,
            oldTruckRow.senhalwireless,
            oldTruckRow.calidadwireless,
            oldTruckRow.tempeje1,
            oldTruckRow.tempeje2,
            oldTruckRow.tempeje3,
            oldTruckRow.tempeje4,
            oldTruckRow.tempeje5,
            oldTruckRow.tempeje6,
            oldTruckRow.presllanta1,
            oldTruckRow.presllanta2,
            oldTruckRow.presllanta3,
            oldTruckRow.presllanta4,
            oldTruckRow.presllanta5,
            oldTruckRow.presllanta6,
            oldTruckRow.velocidad,
            oldTruckRow.isload,
            oldTruckRow.tonelaje,
            oldTruckRow.marcha,
            oldTruckRow.incl_roll,
            oldTruckRow.incl_pitch,
            oldTruckRow.latitude,
            oldTruckRow.longitud,
            oldTruckRow.xcoor,
            oldTruckRow.ycoor,
            oldTruckRow.zcoor,
            oldTruckRow.precisiongps,
            oldTruckRow.tramosids,
            oldTruckRow.direccion,
            oldTruckRow.combustibleint,
            oldTruckRow.templlanta1,
            oldTruckRow.templlanta2,
            oldTruckRow.templlanta3,
            oldTruckRow.templlanta4,
            oldTruckRow.templlanta5,
            oldTruckRow.templlanta6,
            oldTruckRow.bateriasensorllanta1,
            oldTruckRow.bateriasensorllanta2,
            oldTruckRow.bateriasensorllanta3,
            oldTruckRow.bateriasensorllanta4,
            oldTruckRow.bateriasensorllanta5,
            oldTruckRow.bateriasensorllanta6,
            oldTruckRow.tiem_creac,
            oldTruckRow.tiem_update,
            oldTruckRow.segment_angle);


      END IF;

    END LOOP;

  DELETE FROM ta_datacamion where id in ( SELECT id FROM ta_datacamion as da WHERE tiem_creac < applicationTime 
  					and (select count(id) from ta_datacamion where tiem_creac > da.tiem_creac and id_equipo = da.id_equipo ) > 2
  					and id_equipo in (
					select  id_equipo from ts_equipos te 
					where outside_tracking = true 
					and tiem_elimin is null));

  RAISE NOTICE 'Executing process_historic_data truck took %, inserted: %  updated %',
    EXTRACT(MILLISECONDS FROM clock_timestamp() - startTime), insertedRecords, updatedRecords;

  startTime := clock_timestamp();
  insertedRecords := 0;
  updatedRecords := 0;
  FOR oldShovelRow IN SELECT * FROM ta_datapala dp WHERE tiem_creac < applicationTime
  					and (select count(id) from ta_datapala where tiem_creac > dp.tiem_creac and id_equipo = dp.id_equipo ) > 2
  					and id_equipo in (
					 select  id_equipo from ts_equipos te 
					 where outside_tracking = true 
					 and tiem_elimin is null)
    LOOP
      SELECT * INTO historicShovelRow
      FROM ta_datapala_historic
      WHERE id_equipo = oldShovelRow.id_equipo
        AND tiem_creac = oldShovelRow.tiem_creac;

      IF (historicShovelRow.id IS NULL)
      THEN
        insertedRecords := insertedRecords + 1;
        INSERT INTO ta_datapala_historic (id,
                          id_equipo,
                          frecuencia,
                          id_trabajador,
                          senhalgps,
                          senhalwireless,
                          calidadwireless,
                          incl_roll,
                          incl_pitch,
                          xcoor,
                          ycoor,
                          zcoor,
                          precisiongps,
                          direccion,
                          latitude,
                          longitud,
                          combustible,
                          presaceite_motor_iz,
                          temsaceite_motor_iz,
                          velo_motor_iz,
                          presaceite_motor_der,
                          temsaceite_motor_der,
                          velo_motor_der,
                          tiem_creac,
                          tiem_update)

        VALUES (((SELECT (coalesce(max(id), 0)) + 1 FROM public.ta_datapala_historic)),
            oldShovelRow.id_equipo,
            oldShovelRow.frecuencia,
            oldShovelRow.id_trabajador,
            oldShovelRow.senhalgps,
            oldShovelRow.senhalwireless,
            oldShovelRow.calidadwireless,
            oldShovelRow.incl_roll,
            oldShovelRow.incl_pitch,
            oldShovelRow.xcoor,
            oldShovelRow.ycoor,
            oldShovelRow.zcoor,
            oldShovelRow.precisiongps,
            oldShovelRow.direccion,
            oldShovelRow.latitude,
            oldShovelRow.longitud,
            oldShovelRow.combustible,
            oldShovelRow.presaceite_motor_iz,
            oldShovelRow.temsaceite_motor_iz,
            oldShovelRow.velo_motor_iz,
            oldShovelRow.presaceite_motor_der,
            oldShovelRow.temsaceite_motor_der,
            oldShovelRow.velo_motor_der,
            oldShovelRow.tiem_creac,
            oldShovelRow.tiem_update);


      END IF;

    END LOOP;

  DELETE FROM ta_datapala WHERE id in (
 	SELECT id FROM ta_datapala dp WHERE tiem_creac < applicationTime
  					and (select count(id) from ta_datapala where tiem_creac > dp.tiem_creac and id_equipo = dp.id_equipo ) > 2
  					and id_equipo in (
					 select  id_equipo from ts_equipos te 
					 where outside_tracking = true 
					 and tiem_elimin is null));

  RAISE NOTICE 'Executing process_historic_data shovel took %, inserted: %  updated %',
    EXTRACT(MILLISECONDS FROM clock_timestamp() - startTime), insertedRecords, updatedRecords;


  startTime := clock_timestamp();
  insertedRecords := 0;
  updatedRecords := 0;
  FOR oldAuxiliaryRow IN SELECT *
               FROM ta_data_auxiliares dx
               WHERE tiem_creac < applicationTime
               and (select count(id) from ta_data_auxiliares where tiem_creac > dx.tiem_creac and id_equipo = dx.id_equipo ) > 2
  					and id_equipo in (
					 select  id_equipo from ts_equipos te 
					 where outside_tracking = true 
					 and tiem_elimin is null)
               
    LOOP
      SELECT * INTO historicAuxiliaryRow
      FROM ta_data_auxiliares_historic
      WHERE id_equipo = oldAuxiliaryRow.id_equipo
        AND tiem_creac = oldAuxiliaryRow.tiem_creac;

      IF (historicAuxiliaryRow.id IS NULL)
      THEN
        insertedRecords := insertedRecords + 1;
        INSERT INTO ta_data_auxiliares_historic (id,
                             id_equipo,
                             frecuencia,
                             id_trabajador,
                             senhalgps,
                             senhalwireless,
                             calidadwireless,
                             incl_roll,
                             incl_pitch,
                             xcoor,
                             ycoor,
                             zcoor,
                             precisiongps,
                             direccion,
                             latitude,
                             longitud,
                             combustibleint,
                             tiem_creac,
                             tiem_update)

        VALUES (((SELECT (coalesce(max(id), 0)) + 1 FROM public.ta_data_auxiliares_historic)),
            oldAuxiliaryRow.id_equipo,
            oldAuxiliaryRow.frecuencia,
            oldAuxiliaryRow.id_trabajador,
            oldAuxiliaryRow.senhalgps,
            oldAuxiliaryRow.senhalwireless,
            oldAuxiliaryRow.calidadwireless,
            oldAuxiliaryRow.incl_roll,
            oldAuxiliaryRow.incl_pitch,
            oldAuxiliaryRow.xcoor,
            oldAuxiliaryRow.ycoor,
            oldAuxiliaryRow.zcoor,
            oldAuxiliaryRow.precisiongps,
            oldAuxiliaryRow.direccion,
            oldAuxiliaryRow.latitude,
            oldAuxiliaryRow.longitud,
            oldAuxiliaryRow.combustibleint,
            oldAuxiliaryRow.tiem_creac,
            oldAuxiliaryRow.tiem_update);


      END IF;

    END LOOP;

  DELETE FROM ta_data_auxiliares WHERE id in (
 	SELECT id
               FROM ta_data_auxiliares dx
               WHERE tiem_creac < applicationTime
               and (select count(id) from ta_data_auxiliares where tiem_creac > dx.tiem_creac and id_equipo = dx.id_equipo ) > 2
  					and id_equipo in (
					 select  id_equipo from ts_equipos te 
					 where outside_tracking = true 
					 and tiem_elimin is null)
  );

  RAISE NOTICE 'Executing process_historic_data auxiliary took %, inserted: %  updated %',
    EXTRACT(MILLISECONDS FROM clock_timestamp() - startTime), insertedRecords, updatedRecords;


END;
$function$
;

-- Permissions

ALTER FUNCTION public.process_historic_data_tracking() OWNER TO controlsys;
GRANT ALL ON FUNCTION public.process_historic_data_tracking() TO controlsys;



CREATE OR REPLACE VIEW public.equipment_tracks_gps
AS SELECT te.id,
    te.nombre,
    te.ipequipo,
    tdh.cant,
    tdh.tiem_creac,
    te.placa
   FROM ts_equipos te
     LEFT JOIN LATERAL ( SELECT array_length(tdh_1.latitude, 1) AS cant,
            tdh_1.tiem_creac
           FROM ta_datacamion tdh_1
          WHERE tdh_1.id_equipo = te.id_equipo
          ORDER BY tdh_1.tiem_creac DESC
         LIMIT 1) tdh ON true
  WHERE te.isflota = false AND te.ipequipo::text <> '0.0.0.0'::text AND length(te.ipequipo::text) > 0 AND te.tiem_elimin IS NULL AND te.outside_tracking = true AND tdh.cant IS NOT NULL AND te.id = 76
  ORDER BY tdh.tiem_creac desc;

-- Permissions

ALTER TABLE public.equipment_tracks_gps OWNER TO controlsys;
GRANT ALL ON TABLE public.equipment_tracks_gps TO controlsys;
