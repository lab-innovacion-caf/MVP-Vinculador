# Databricks notebook source
# Unmount directory if previously mounted.
MOUNTPOINT = "/mnt/poc-vinculador-files"
if MOUNTPOINT in [mnt.mountPoint for mnt in dbutils.fs.mounts()]:
  dbutils.fs.unmount(MOUNTPOINT)

# Add the Storage Account, Container, and reference the secret to pass the SAS Token
STORAGE_ACCOUNT = 'sapocvinculadorcr'
CONTAINER = "poc-vinculador-files"
SASTOKEN = "sp=racwdl&st=2024-12-04T16:14:23Z&se=2026-12-02T00:14:23Z&spr=https&sv=2022-11-02&sr=c&sig=nlSqODWL9VqplujSbRPl7YBE8rQb26dB4p9V3lsWp8g%3D"

SOURCE = "wasbs://{container}@{storage_acct}.blob.core.windows.net/".format(container=CONTAINER, storage_acct=STORAGE_ACCOUNT)
URI = "fs.azure.sas.{container}.{storage_acct}.blob.core.windows.net".format(container=CONTAINER, storage_acct=STORAGE_ACCOUNT)

try:
  dbutils.fs.mount(
    source=SOURCE,
    mount_point=MOUNTPOINT,
    extra_configs={URI:SASTOKEN})
except Exception as e:
  if "Directory already mounted" in str(e):
    pass # Ignore error if already mounted.
  else:
    raise e

# COMMAND ----------

# Unmount directory if previously mounted.
MOUNTPOINT = "/mnt/poc-vinculador-gpt-files"
if MOUNTPOINT in [mnt.mountPoint for mnt in dbutils.fs.mounts()]:
  dbutils.fs.unmount(MOUNTPOINT)

# Add the Storage Account, Container, and reference the secret to pass the SAS Token
STORAGE_ACCOUNT = 'sapocvinculadorcr'
CONTAINER = "poc-vinculador-gpt-files"
SASTOKEN = "sp=racwdl&st=2024-12-05T07:56:10Z&se=2026-12-01T15:56:10Z&spr=https&sv=2022-11-02&sr=c&sig=D2JcZ4Fov03K2XKvY04mtf9Mm93GyYGBw0ntdmkl6Xw%3D"

SOURCE = "wasbs://{container}@{storage_acct}.blob.core.windows.net/".format(container=CONTAINER, storage_acct=STORAGE_ACCOUNT)
URI = "fs.azure.sas.{container}.{storage_acct}.blob.core.windows.net".format(container=CONTAINER, storage_acct=STORAGE_ACCOUNT)

try:
  dbutils.fs.mount(
    source=SOURCE,
    mount_point=MOUNTPOINT,
    extra_configs={URI:SASTOKEN})
except Exception as e:
  if "Directory already mounted" in str(e):
    pass # Ignore error if already mounted.
  else:
    raise e

# COMMAND ----------

dbutils.fs.mounts()
