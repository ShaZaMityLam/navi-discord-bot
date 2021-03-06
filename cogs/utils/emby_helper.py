#!/usr/bin/env python3

from discord import Embed
import hashlib
import asyncio
import requests
import aiohttp
from cogs.utils.config import Config
from embypy import Emby as EmbyPy

colours = [0x1f8b4c, 0xc27c0e, 0x3498db, 0x206694, 0x9b59b6,
           0x71368a, 0xe91e63, 0xe67e22, 0xf1c40f, 0x1abc9c,
           0x2ecc71, 0xa84300, 0xe74c3c, 0xad1457, 0x11806a]

conf = Config('configs/emby.json')

if 'address' not in conf or not conf['address']:
  conf['address'] = input('Enter emby url: ')
  conf.save()
if 'watching' not in conf or 'last' not in conf['watching']:
  conf['watching'] = {'last':None}
  conf.save()
if 'auth' not in conf or not conf['auth']:
  conf['auth'] = {}
  conf['auth']['api_key']   = input('Enter emby api key: ')
  conf['auth']['userid']    = input('Enter emby user id: ')
  conf['auth']['device_id'] = input('Enter emby device id: ')
  conf.save()

conn = EmbyPy(conf['address'], **conf['auth'], ws=False)

async def makeEmbed(item, message=''):
  loop = asyncio.get_event_loop()
  if hasattr(item, 'index_number'):
    name = '{:02} - {}'.format(item.index_number, item.name)
  else:
    name = item.name or ''
  em = Embed()
  async with aiohttp.get(item.primary_image_url) as img:
    if img.status == 200:
      em.set_thumbnail(url=img.url)
    elif item.parent:
      em.set_thumbnail(url=item.parent.primary_image_url)
  em.title  = (message+name or '<No name>').strip()
  if hasattr(item, 'overview') and item.overview:
    if len(item.overview) > 250:
      des = item.overview[:247] + '...'
    else:
      des = item.overview
    em.description = des
  elif item.id:
    em.description = item.media_type
  if item.id:
    em.url         = item.url
  em.colour        = getColour(item.id)
  if hasattr(item, 'artist_names'):
    if len(item.artist_names) == 1:
      em.add_field(name='Artist', value=item.artist_names[0])
    elif len(item.artist_names) > 1:
      em.add_field(name='Artists', value=', '.join(item.artist_names))
  if hasattr(item, 'album'):
    a = item.album
    if a and a.name:
      em.add_field(name='Album', value=a.name)
  if hasattr(item, 'genres') and item.genres:
    em.add_field(name='Tags', value=', '.join(item.genres))
  if hasattr(item, 'genres') and item.genres:
    em.add_field(name='Tags', value=', '.join(item.genres))
  if item.object_dict.get('RunTimeTicks', None):
    d = int(float(item.object_dict.get('RunTimeTicks') / (10**7)))
    if d > 1:
      d = '{:02}:{:02}:{:02}'.format(d//3600, d//60, d%60)
      em.add_field(name='Duration', value=d)
  return em

def getColour(string : str):
  str_hash = hashlib.md5()
  str_hash.update(string.strip().encode())
  str_hash = int(str_hash.hexdigest(), 16)
  return colours[str_hash % len(colours)]
