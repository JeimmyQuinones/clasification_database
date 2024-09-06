from typing import List
import uuid
from sqlalchemy.orm import Session
from api.domain.entities.report_total_version import (
    ReportDetailVersionEntity,
    ReportTotalVersionEntity,
    ReportTypeVersionEntity,
)
from api.domain.entities.scan_table_info import (
    ScanDetailTableEntity,
    ScanDomainEntity,
    ScanTableEntity,
)
from api.domain.repositories.database_repository_interface import (
    DatabaseRepositoryInterface,
)
from api.infrastructure.database.connector import get_db_connection
from api.infrastructure.database.models import (
    DatabaseDBModel,
    ScanTablesDBModel,
    ScanDetailTablesDBModel,
    ScanDomainDBModel,
)
from api.domain.entities.databaseC import DatabaseEntity, ScanDatabaseById

from sqlalchemy import and_, text


class DatabaseRepositoryImpl(DatabaseRepositoryInterface):
    def create_databasec(self, database: DatabaseEntity) -> None:
        session: Session = next(get_db_connection())
        db_data = DatabaseDBModel(
            id=str(database.id),
            user_create_id=database.user_id,
            host=database.host,
            port=database.port,
            username=database.username,
            password=database.password,
        )
        session.add(db_data)
        session.commit()
        session.close()

    def get_databasec_by_host_port(self, host: str, port: str) -> None:
        session: Session = next(get_db_connection())
        db_data = (
            session.query(DatabaseDBModel)
            .filter(and_(DatabaseDBModel.host == host, DatabaseDBModel.port == port))
            .first()
        )
        session.close()
        if db_data is None:
            return None
        return DatabaseEntity(
            id=uuid.UUID(db_data.id),
            host=db_data.host,
            port=db_data.port,
            username=db_data.username,
            password=db_data.password,
            user_id=db_data.user_create_id,
        )

    def get_databasec_by_id(self, id: str) -> None:
        session: Session = next(get_db_connection())
        db_data = (
            session.query(DatabaseDBModel).filter(DatabaseDBModel.id == id).first()
        )
        session.close()
        if db_data is None:
            return None
        return DatabaseEntity(
            id=uuid.UUID(db_data.id),
            host=db_data.host,
            port=db_data.port,
            username=db_data.username,
            password=db_data.password,
            user_id=db_data.user_create_id,
            date_scan=db_data.date_scan,
            lates_scan_version=db_data.lates_version,
        )

    def Add_domain_scan_list(self, data: List[ScanDomainEntity]) -> None:
        try:
            session: Session = next(get_db_connection())
            for domain_entity in data:
                db_data = ScanDomainDBModel(
                    id=domain_entity.id,
                    name=domain_entity.name,
                    database_id=domain_entity.database_id,
                    version_scan=domain_entity.version,
                )
                session.add(db_data)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def Add_tables_scan_list(self, data: List[ScanTableEntity]) -> None:
        try:
            session: Session = next(get_db_connection())
            for domain_entity in data:
                db_data = ScanTablesDBModel(
                    id=domain_entity.id,
                    name=domain_entity.name,
                    domain_id=domain_entity.domain_id,
                )
                session.add(db_data)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def Add_tables_detail_scan_list(self, data: List[ScanDetailTableEntity]) -> None:
        try:
            session: Session = next(get_db_connection())
            for domain_entity in data:
                db_data = ScanDetailTablesDBModel(
                    id=domain_entity.id,
                    nameColumn=domain_entity.nameColumn,
                    table_id=domain_entity.table_id,
                    typeIdentified_id=domain_entity.typeIdentified_id,
                )
                session.add(db_data)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def Update_databasec(self, database: DatabaseEntity) -> None:
        session: Session = next(get_db_connection())
        db_data = (
            session.query(DatabaseDBModel)
            .filter(DatabaseDBModel.id == str(database.id))
            .one_or_none()
        )
        db_data.date_scan = database.date_scan
        db_data.lates_version = database.lates_scan_version
        session.commit()
        session.close()

    def get_scan_data_by_id(self, id: str, last_version: int):
        session: Session = next(get_db_connection())
        sql_query = """
            SELECT 
                d.id AS database_id,
                d.date_scan AS database_date_scan,
                sd.id AS domain_id,
                sd.name AS domain_name,
                st.name AS table_name,
                sdt.nameColumn AS detail_column_name,
                tid.name AS type_description
            FROM 
                databaseScan d
            JOIN 
                scanDomain sd ON d.id = sd.database_id
            JOIN 
                scanTables st ON sd.id = st.domain_id
            JOIN 
                scanDetailTables sdt ON st.id = sdt.table_id
            LEFT JOIN 
                typeIdentifiedData tid ON sdt.typeIdentified_id = tid.id
            WHERE 
                d.id = :database_id AND sd.version_scan =:last_version;
        """
        result = session.execute(
            text(sql_query), {"database_id": id, "last_version": last_version}
        )
        rows = result.fetchall()
        session.close()
        domains_list: List[ReportTotalVersionEntity] = []
        for row in rows:
            domain_id = row[2]
            domain_name = row[3]
            table_name = row[4]
            detail_column_name = row[5]
            type_description = row[6]
            reporte = ScanDatabaseById(
                domain_id=domain_id,
                domain_name=domain_name,
                table_name=table_name,
                detail_column_name=detail_column_name,
                type_description=type_description,
            )
            domains_list.append(reporte)
        return domains_list

    def get_report_totals_info_version(self, id: str):
        session: Session = next(get_db_connection())
        sql_query = """
            SELECT
                COUNT(DISTINCT st.id) AS total_tablas,
                COUNT(sdt.id) AS total_columnas,
                COUNT(CASE WHEN tipo_tipo.name != "N/A" THEN 1 END) AS total_clasificadas,
                sd.version_scan AS version,
                sd.date_scan  AS date_scan,
                COUNT(DISTINCT sd.id) AS total_schemes
            FROM scanTables st
            JOIN scanDomain sd ON st.domain_id = sd.id
            JOIN databaseScan d ON sd.database_id = d.id
            LEFT JOIN  scanDetailTables sdt ON st.id = sdt.table_id
            LEFT JOIN typeIdentifiedData tipo_tipo ON sdt.typeIdentified_id = tipo_tipo.id
            WHERE d.id = :database_id
            GROUP BY sd.version_scan , sd.date_scan
            ORDER BY sd.version_scan;
        """
        result = session.execute(text(sql_query), {"database_id": id})
        rows = result.fetchall()
        session.close()
        list_report: List[ReportTotalVersionEntity] = []
        for row in rows:
            total_tablas = row[0]
            total_columnas = row[1]
            total_clasificadas = row[2]
            version_scan = row[3]
            date_scan = row[4]
            total_schemes = row[5]
            reporte = ReportTotalVersionEntity(
                total_tablas=total_tablas,
                total_columnas=total_columnas,
                total_clasificadas=total_clasificadas,
                version_scan=version_scan,
                date_scan=date_scan,
                total_schemes=total_schemes,
            )
            list_report.append(reporte)

        return list_report

    def get_report_types_info(self, id: str):
        session: Session = next(get_db_connection())
        sql_query = """
            SELECT
                tipo_tipo.name AS name_tipo,
                COUNT(sdt.id) AS total_columnas,
                sd.version_scan AS version_scan
            FROM  typeIdentifiedData tipo_tipo
            LEFT JOIN scanDetailTables sdt ON sdt.typeIdentified_id = tipo_tipo.id
            JOIN  scanTables st ON st.id = sdt.table_id
            JOIN  scanDomain sd ON st.domain_id = sd.id
            JOIN databaseScan d ON sd.database_id = d.id
            WHERE  d.id = :database_id
            GROUP BY tipo_tipo.name, sd.version_scan;
        """

        result = session.execute(text(sql_query), {"database_id": id})
        rows = result.fetchall()
        session.close()
        list_response: List[ReportTypeVersionEntity] = []
        for row in rows:
            name_tipo = row[0]
            total_columnas = row[1]
            version_scan = row[2]
            reporte = ReportTypeVersionEntity(
                name_tipo=name_tipo,
                total_columnas=total_columnas,
                version_scan=version_scan,
            )
            list_response.append(reporte)
        return list_response

    def get_report_by_version_detail(self, id: str, version: int):
        session: Session = next(get_db_connection())
        sql_query = """
            SELECT
                sd.name AS domain_name,
                sd.id AS domain_id,
                st.name AS table_name,
                COUNT(sdt.id) AS columns,
                COUNT(CASE WHEN tipo_tipo.name != "N/A" THEN 1 END) AS total_clasification
            from scanTables st
            JOIN scanDomain sd ON st.domain_id = sd.id
            JOIN databaseScan d ON sd.database_id = d.id
            LEFT JOIN scanDetailTables sdt ON st.id = sdt.table_id
            LEFT JOIN typeIdentifiedData tipo_tipo ON sdt.typeIdentified_id = tipo_tipo.id
            WHERE d.id = :database_id AND sd.version_scan = :version
            group by sd.name, sd.id, st.name
        """
        result = session.execute(
            text(sql_query), {"database_id": id, "version": version}
        )
        rows = result.fetchall()
        session.close()
        list_response: List[ReportDetailVersionEntity] = []
        for row in rows:
            domain_name = row[0]
            domain_id = row[1]
            table_name = row[2]
            columns = row[3]
            total_clasification = row[4]
            reporte = ReportDetailVersionEntity(
                domain_name=domain_name,
                domain_id=domain_id,
                table_name=table_name,
                columns=columns,
                total_clasification=total_clasification,
            )
            list_response.append(reporte)
        return list_response
