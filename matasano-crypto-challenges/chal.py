import base64
import binascii

ASCII_CHARS = range(ord('a'), ord('z')) + range(ord('A'), ord('Z')) + [ord(' ')]


def bytes_to_hex(byt):
    return binascii.hexlify(byt)

def hex_to_bytes(hexstr):
    return(bytearray.fromhex(hexstr))

def bytes_xor_someint(byt, i):
    result = bytearray()
    for ch in byt:
        result.append(i ^ ch)
    return result

def english_score(byt):
    score = 0
    for b in byt:
        if b in ASCII_CHARS:
            score = score + 1
    return score



# chal 1
hex_str = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
b64_str = 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'
byt = bytearray.fromhex(hex_str)
newb64str = base64.b64encode(byt)
assert (newb64str == b64_str)

# chal 2
x = '1c0111001f010100061a024b53535009181c'
y = '686974207468652062756c6c277320657965'
expected = '746865206b696420646f6e277420706c6179'
bx = bytearray.fromhex(x)
by = bytearray.fromhex(y)
foo = bytearray()
for i in range(len(bx)):
    foo.append(bx[i] ^ by[i])

z = bytes_to_hex(foo)
assert (z == expected)


# chal 3
hex_str = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
byt = hex_to_bytes(hex_str)
result = list()
scores = list()
for i in ASCII_CHARS:
    r = bytes_xor_someint(byt, i)
    result.append(r)
    scores.append(english_score(r))

idx_max = scores.index(max(scores))
final_result = result[idx_max]
print final_result
