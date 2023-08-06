import os
import logging

import CloudFlare


logger = logging.getLogger(__name__)


def update_record(zone_name, record_name, record_type, record_address):
    CLOUDFLARE_API_TOKEN = os.environ["CLOUDFLARE_TOKEN"]
    cf = CloudFlare.CloudFlare(token=CLOUDFLARE_API_TOKEN)

    record = {
        "name": record_name,
        "type": record_type,
        "content": record_address,
        "ttl": 1,
        "proxied": False,
    }

    zone_id = None
    for zone in cf.zones.get():
        if zone["name"] == zone_name:
            zone_id = zone["id"]
            break
    else:
        raise ValueError(f"Cloudflare zone {zone_name} not found")

    for _record in cf.zones.dns_records.get(zone_id):
        if _record["name"] == record_name:
            logger.info(
                f"record name={record_name} type={record_type} address={record_address} already exists updating"
            )
            cf.zones.dns_records.put(zone_id, _record["id"], data=_record)
            break
    else:
        logger.info(
            f"record name={record_name} type={record_type} address={record_address} does not exists creating"
        )
        cf.zones.dns_records.post(zone_id, data=record)
