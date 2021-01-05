---------------------------------------------------------------------------------
--                                     hex                                     --
---------------------------------------------------------------------------------

function string.fromhex(str)
  return (str:gsub(
    "..",
    function(cc)
      return string.char(tonumber(cc, 16))
    end
  ))
end

function string.tohex(str)
  return (str:gsub(
    ".",
    function(c)
      return string.format("\\x%02X", string.byte(c))
    end
  ))
end

--[[

> string.tohex('AAAA')
\x41\x41\x41\x41

--]]