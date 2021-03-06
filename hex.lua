---------------------------------------------------------------------------------
--                                     hex                                     --
---------------------------------------------------------------------------------

local string = require "string"

function string.tohex(str)
  return (str:gsub(
    ".",
    function(c)
      return string.format("%02X", string.byte(c))
    end
  ))
end

function string.hexlify(str)
  return (str:gsub(
    "..",
    function(cc)
      return string.format("\\x%s", cc)
    end
  ))
end

function string.fromhex(str)
  return (str:gsub(
    "..",
    function(cc)
      return string.char(tonumber(cc, 16))
    end
  ))
end

function string.startswith(s, n)
  return s:sub(1, #n) == n
end

function string.endswith(self, str)
  -- return self:sub(-#str) == str
  return self:sub(-(#str)) == str
end

--[[

  local p = "AAAA"
  local hex_p = string.tohex(p)

  print(p:tohex())
  print(p:tohex():hexlify())
  print(hex_p:fromhex())
  > lua test2.lua
  > 41414141
  > \x41\x41\x41\x41
  > AAAA

--]]
