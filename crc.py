import sys

def crc_update(crc, data):
  crc ^= (data << 8)
  for x in range(8):
    if (crc & 0x8000) == 0x8000: crc = ((crc << 1) ^ 0x1021) & 0xFFFF
    else: crc <<= 1
  crc &= 0xFFFF
  return crc

path = sys.argv[1]
with open(path, 'rb') as f:
  data = f.read()
crc = 0xFFFF
data = list(data)
print 'cur: %.2x%.2x' % (ord(data[0x67FE]), ord(data[0x67FF]))
data[0x67FE] = data[0x67FF] = '\xff'
data = data[:0x67FE]
for x in range(len(data)):
  crc = crc_update(crc, ord(data[x]))
  #if crc == 0x8114 or crc == 0x1481:
   #   print '%x %x' % (crc, x)

print 'new: %.4x' % crc
