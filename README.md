# OIV-Package-Generator
An external tool working together with OpenIV to automatically generate an `.oiv` package for GTA:V modding. 

This is useful for those who need to release their own HUGE modding compilation.



### Requirement
1. OpenIV installed
2. Python 3
3. An UNMODIFIED copy of GTA (only ADD is allowed, for example, the `mods` folder is allowed).
4. One-time 2 hours' Patience for human interaction due to the lack of OpenIV API. (After the first initial setup, the future run will be very much faster)
5. Around 10GB-100GB temporary disk space depending on your diff scale. SSD is far better than HDD.


### Explaination
The tool will assume your game is left untouched

#### opg-compare.py
It keeps a file tree of GTA:V to help identify files possibly related to modding

For `RPF` files especially, the tool assume `RPF` files are only modded in `mods` folder. It compares the two copies of extracted RPF archives and helps you identify which ones are modded.

#### HUMAN INTERACTION
Once the modded RPF files are found, the next step requires you to extract the **BOTH** copies of RPF files in a folder.

##### Tips 1
In this step, you can decide how deep the comparation&packaging goes:
1. you may decide to leave the whole rpf files untouched because it's too small to bother.
`In this case, you can delete the automatically created xxx.rpf folder, and copy the xxx.rpf file itself.`

2. or you need to extract the nested rpf files too, to cut down the final OIV package size.
`In this case, you need to delete the file and create a new rpf directory`

The more you extracted, the more space you will be able to save in the final package.

If a RPF archive did not change, you will only need to extract it for once.

##### Tips 2
Since opg-generate.py is some kind of diff tool, you can make a patch not only based on the original files, but also on any **common** base(redux for example).


##### Tips 3
Before you run the final packing, make a full check and delete the files you dont want, make sure you are not to mess up the users game.


#### opg-generate.py
After the RPF files extracted, this script helps you find what's different between them and generate the final OIV package.

This will take a long time, varies from 10 minutes to 2 hours. During this time, you can custom the `assembly-template.xml` files (without tag `content`) and update the `icon.png`.

