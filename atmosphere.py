import sys, math
import numpy as np

def airMassKastenYoung(altitude, observerElevation = 0):
    if altitude > 0:
        return (airDensity(observerElevation) / 1.28) / (math.sin(math.radians(altitude)) + 0.50572 * (math.radians(altitude) + 6.07995) ** (-1.6364))
    else:
        return 1e6

airMass = airMassKastenYoung

def airDensityLogMSIS(altitude):
    if altitude >= 300000:
        return 0

    f, i = math.modf(altitude / 500)
    i = int(i)

    logs = [
        -6.717961707349481,
        -6.771477660689589,
        -6.824333670843065,
        -6.875288088844636,
        -6.926122936340322,
        -6.976141191848602,
        -7.025750837219845,
        -7.075227632925886,
        -7.124792511864586,
        -7.174458945048726,
        -7.224660210110821,
        -7.27534673466222,
        -7.326761657656969,
        -7.3791999460242765,
        -7.432510808281625,
        -7.487038203393035,
        -7.542633551418106,
        -7.5997031789666005,
        -7.658107933312862,
        -7.717885815027901,
        -7.779072645213561,
        -7.84195543139986,
        -7.906341253583122,
        -7.972256038021479,
        -8.0397175473318,
        -8.108400293215398,
        -8.178936833001524,
        -8.25099015064158,
        -8.324096561454324,
        -8.398965810051587,
        -8.475092015397601,
        -8.552820369059388,
        -8.631482337818365,
        -8.710777940488903,
        -8.790972358699026,
        -8.871727570855859,
        -8.952602175897473,
        -9.033869228860404,
        -9.1159396965547,
        -9.197424146709636,
        -9.277977020691994,
        -9.35872437774244,
        -9.438999103978503,
        -9.51904181165204,
        -9.598800881268524,
        -9.678266161426953,
        -9.757657104324588,
        -9.836576847253502,
        -9.915357725106615,
        -9.994068930767366,
        -10.072379689018423,
        -10.150667681678579,
        -10.228940722674908,
        -10.306954657981619,
        -10.384754374060574,
        -10.462803385462554,
        -10.540254399659966,
        -10.618062680509693,
        -10.695792304629292,
        -10.772894698511433,
        -10.850753088709714,
        -10.927920443029986,
        -11.004903768536971,
        -11.082442593886777,
        -11.159455651980444,
        -11.236810028889913,
        -11.314074606225063,
        -11.389823267836245,
        -11.466041879071378,
        -11.541324939491926,
        -11.616287977965381,
        -11.69061775338052,
        -11.764468490806136,
        -11.837824925238825,
        -11.910720066774173,
        -11.98308910701733,
        -12.054897817733055,
        -12.1261530223543,
        -12.197112904158702,
        -12.267309955001362,
        -12.337320932140127,
        -12.406476709874894,
        -12.47526013534579,
        -12.54378565158752,
        -12.611637758638672,
        -12.678960429955772,
        -12.74598385019126,
        -12.812308454100823,
        -12.878241419704928,
        -12.943798869488086,
        -13.009034692097325,
        -13.073573213234896,
        -13.137984758307285,
        -13.201947856747172,
        -13.265656547230805,
        -13.328772729727373,
        -13.391550867219946,
        -13.45434570875269,
        -13.516888545474158,
        -13.578858656625272,
        -13.64071726759111,
        -13.703075128634486,
        -13.764817443648756,
        -13.825965015868134,
        -13.887436297535864,
        -13.948813405278694,
        -14.010066652426572,
        -14.071435598802863,
        -14.132690101205078,
        -14.193992994742551,
        -14.255256600049313,
        -14.316715938353274,
        -14.37815593046006,
        -14.439691534059497,
        -14.501483534776218,
        -14.563325139866528,
        -14.625416299134415,
        -14.687545198583893,
        -14.7499652604661,
        -14.812740232343781,
        -14.875671660258131,
        -14.938825459272756,
        -15.00229853753611,
        -15.06587640185992,
        -15.130042552857274,
        -15.194630715336164,
        -15.2594340319208,
        -15.32465074908301,
        -15.390064068544874,
        -15.455923274697804,
        -15.522561299265375,
        -15.58923366470623,
        -15.656250209414047,
        -15.724028587802525,
        -15.792395511319018,
        -15.8611305511686,
        -15.929957708842926,
        -15.999424121240821,
        -16.06930548678889,
        -16.14023901564401,
        -16.211417808189694,
        -16.2830882256305,
        -16.355211359839412,
        -16.42802333235742,
        -16.501261251571716,
        -16.575222542390375,
        -16.648953928474548,
        -16.72304882078235,
        -16.797537184462154,
        -16.87226753335604,
        -16.947291675981543,
        -17.02295200520681,
        -17.09919160619859,
        -17.175949947154262,
        -17.253475663818644,
        -17.331445617096854,
        -17.410535436606587,
        -17.490487106909217,
        -17.57138488090249,
        -17.65335416521817,
        -17.736069894414708,
        -17.819648852300226,
        -17.904270741892475,
        -17.99019787286891,
        -18.077091039562287,
        -18.164489338591956,
        -18.25347282496846,
        -18.343719702816237,
        -18.434779668331867,
        -18.526819340014033,
        -18.619741624750617,
        -18.713710422730742,
        -18.80869893845681,
        -18.904539919488542,
        -19.001213780143175,
        -19.09874228709427,
        -19.19720953345136,
        -19.296309494107632,
        -19.396190835486493,
        -19.496553545650986,
        -19.597687100048486,
        -19.699377094474237,
        -19.801390726778354,
        -19.903926631148707,
        -20.00640212976915,
        -20.108620884541423,
        -20.211041192266713,
        -20.313144917302054,
        -20.41431162921909,
        -20.515438989744094,
        -20.615308695441318,
        -20.715297667297236,
        -20.814066201272908,
        -20.911887195888895,
        -21.008816848389237,
        -21.104526256357758,
        -21.1992070588589,
        -21.29260373178007,
        -21.384720570773865,
        -21.475314125426518,
        -21.56468103417546,
        -21.652388547635944,
        -21.738824570479235,
        -21.82408054916972,
        -21.908089822433585,
        -21.99124397124826,
        -22.07342115145043,
        -22.154976061596784,
        -22.23557703864979,
        -22.315846632314088,
        -22.395643549154386,
        -22.474843516541636,
        -22.55397405631304,
        -22.63245840306656,
        -22.711040190100423,
        -22.789988606218472,
        -22.867992845324878,
        -22.94703974951617,
        -23.025850929940457,
        -23.10456951465186,
        -23.183675015134025,
        -23.26309340563417,
        -23.34275586106914,
        -23.422455409616425,
        -23.502275126989115,
        -23.58184827235317,
        -23.66129540037211,
        -23.740630410627517,
        -23.819481649078725,
        -23.897885570560074,
        -23.975698445343454,
        -24.053073222521892,
        -24.129676785661456,
        -24.2054563778181,
        -24.280766213003968,
        -24.35500909968954,
        -24.42827467299023,
        -24.500320981964073,
        -24.571375516630905,
        -24.640804023062667,
        -24.709473740563933,
        -24.776276535675535,
        -24.841698194697603,
        -24.905130996698006,
        -24.967271173722917,
        -25.02685104531373,
        -25.08313966697916,
        -25.13864245130185,
        -25.1930313859283,
        -25.24593480142276,
        -25.298877220692958,
        -25.349455390158578,
        -25.39950247136836,
        -25.448459065534234,
        -25.49649970798176,
        -25.543735420225662,
        -25.589930665632636,
        -25.635504809186475,
        -25.680123425362197,
        -25.724000306365404,
        -25.76709603590031,
        -25.80954104525141,
        -25.851334227934764,
        -25.89248663016004,
        -25.933023026514967,
        -25.972793039325015,
        -26.01222710857042,
        -26.05101201418526,
        -26.08921985221026,
        -26.126721521617753,
        -26.164068851791203,
        -26.200709869391883,
        -26.236758585159482,
        -26.272611958298192,
        -26.30793283071245,
        -26.342891003595888,
        -26.377401371713198,
        -26.411371832217604,
        -26.445008636979605,
        -26.478552154469728,
        -26.511299864050205,
        -26.54414408347886,
        -26.576360714789622,
        -26.60821054067672,
        -26.63962291156759,
        -26.670904904514362,
        -26.70201161164662,
        -26.732894354682063,
        -26.76308064499544,
        -26.793340784636303,
        -26.823206860390478,
        -26.85261409141778,
        -26.881966303430307,
        -26.91123200442218,
        -26.939875938039275,
        -26.968848739668033,
        -26.997093295028574,
        -27.02506714707098,
        -27.05328478687993,
        -27.0805902375702,
        -27.108069312364716,
        -27.135715303820593,
        -27.16289424669567,
        -27.18954557029735,
        -27.21626596091329,
        -27.243041322161403,
        -27.269159645302516,
        -27.295263420245202,
        -27.321332963214154,
        -27.347347064874306,
        -27.372510420777047,
        -27.398323351809527,
        -27.42400694654422,
        -27.448699559134592,
        -27.474017367118883,
        -27.49911604504861,
        -27.523063974423454,
        -27.548519894416806,
        -27.572752207804573,
        -27.596619689211217,
        -27.62107078507538,
        -27.64522146532969,
        -27.669138438041678,
        -27.692896519646634,
        -27.716579004290196,
        -27.740166563189344,
        -27.763638640543387,
        -27.786973417702434,
        -27.810147781825982,
        -27.833259706562863,
        -27.856291928258933,
        -27.879226097838128,
        -27.901911625740492,
        -27.924587131539305,
        -27.947239846522518,
        -27.96971582040286,
        -27.99199098415016,
        -28.01433341939558,
        -28.036586229037045,
        -28.058578470511527,
        -28.080594863662775,
        -28.10246578297069,
        -28.124334314609907,
        -28.146189489128677,
        -28.16784854223354,
        -28.189287814294676,
        -28.21083961118149,
        -28.232318642858615,
        -28.25352345691916,
        -28.27480686695077,
        -28.295969642129815,
        -28.316994092740494,
        -28.338064401680604,
        -28.35896680203119,
        -28.379892445260854,
        -28.40083338142398,
        -28.42156064249714,
        -28.44205133714521,
        -28.462740946352433,
        -28.48316402797895,
        -28.50377354578822,
        -28.524083721683496,
        -28.544565622134677,
        -28.564712362482872,
        -28.585013714986715,
        -28.60494096063934,
        -28.625273389272415,
        -28.645200348621827,
        -28.66525114566739,
        -28.685138164710107,
        -28.70484323578944,
        -28.72464586308562,
        -28.744544017332412,
        -28.764224849366276,
        -28.783667293089145,
        -28.80317230793153,
        -28.822736022858983,
        -28.842354274660778,
        -28.86168018551699,
        -28.881037858755892,
        -28.90042172557694,
        -28.919825855771183,
        -28.938874050741877,
        -28.957915133766992,
        -28.97732582883228,
        -28.996337070663248,
        -29.015317474385764,
        -29.03425819777875,
        -29.053149930057653,
        -29.07198287839075,
        -29.090746755134322,
        -29.109430765956244,
        -29.128470526414603,
        -29.14696868527531,
        -29.16581548536688,
        -29.184551396424354,
        -29.203163243618953,
        -29.22163727412206,
        -29.239959153321,
        -29.25862299899032,
        -29.276604474999,
        -29.294915214158706,
        -29.313567500183286,
        -29.33202622188814,
        -29.350273894369856,
        -29.368292399872534,
        -29.38664153854073,
        -29.404744222670505,
        -29.422580605153936,
        -29.440740910533595,
        -29.45861503816582,
        -29.47681447364909,
        -29.49470632472819,
        -29.51226775165814,
        -29.530143103485102,
        -29.54834380813195,
        -29.56618916845196,
        -29.58365381074469,
        -29.601428896584263,
        -29.619525662616283,
        -29.63721219586879,
        -29.6544604674931,
        -29.672011471234132,
        -29.689876023999997,
        -29.707267766711865,
        -29.724967343811265,
        -29.74215974435164,
        -29.759652901799157,
        -29.77660246011293,
        -29.793844266547435,
        -29.811388576198343,
        -29.82924619359835,
        -29.84651150207166,
        -29.863147745274034,
        -29.881013758803423,
        -29.897274279675205,
        -29.914784454682007,
        -29.93160820625992,
        -29.949024461650975,
        -29.966129400628155,
        -29.983111628826432,
        -30.000066575622863,
        -30.01709651942162,
        -30.03397918306938,
        -30.050926851499135,
        -30.067709193446074,
        -30.084545384487882,
        -30.101433319566095,
        -30.11813018927175,
        -30.1348659667368,
        -30.151637848350628,
        -30.16831639660827,
        -30.185020642203835,
        -30.201616381576912,
        -30.218226307338554,
        -30.234846445973226,
        -30.251335202726672,
        -30.267820995502593,
        -30.28429908118378,
        -30.300764482876172,
        -30.317211982677865,
        -30.33363611454082,
        -30.3500311572671,
        -30.36639112768572,
        -30.382709774060586,
        -30.398980569784666,
        -30.415358585202878,
        -30.43151560742204,
        -30.447770733954098,
        -30.463954499177447,
        -30.480059010331736,
        -30.49625158141838,
        -30.512353849174044,
        -30.528538341985584,
        -30.54462055994402,
        -30.56059118722887,
        -30.576630780079327,
        -30.592545218152804,
        -30.60852062122148,
        -30.624555805939053,
        -30.64044671661454,
        -30.65618220017335,
        -30.67216925301302,
        -30.68799069895373,
        -30.703850439867505,
        -30.719526789634894,
        -30.735229865818624,
        -30.750956992941845,
        -30.766705349909984,
        -30.78247196448196,
        -30.79801631891976,
        -30.813806120652394,
        -30.8293592895792,
        -30.84490939928571,
        -30.860452454736265,
        -30.875984275560068,
        -30.891500490651826,
        -30.906996532837322,
        -30.922467633631584,
        -30.93790881811996,
        -30.953314899995238,
        -30.968680476786716,
        -30.98399992532023,
        -30.999557715351155,
        -31.014771583986985,
        -31.03022049492803,
        -31.04530373713936,
        -31.0606179721124,
        -31.075856954620534,
        -31.09101354410121,
        -31.10608034618916,
        -31.121377633910523,
        -31.136579512915446,
        -31.151677937628033,
        -31.166664594143626,
        -31.18187927214511,
        -31.196975223205186,
        -31.211943428537392,
        -31.226774592053,
        -31.241829034622327,
        -31.256737995084844,
        -31.2718726010319,
        -31.286465793956246,
        -31.301667801781424,
        -31.316307034532354,
        -31.331163762321196,
        -31.346244545382085,
        -31.36072256456274,
        -31.37583620237279,
        -31.39032303433903,
        -31.40502282345932,
        -31.419941924222712,
        -31.434638247512908,
        -31.449098508514165,
        -31.463770940462187,
        -31.478661862427426,
        -31.49330202946188,
        -31.507676977519402,
        -31.522261582174167,
        -31.536565155258984,
        -31.55107629305396,
        -31.56580110847931,
        -31.58022691248441,
        -31.594863870086492,
        -31.609183923861238,
        -31.623712024424147,
        -31.637904402380656,
        -31.652301107293646,
        -31.66690810857908,
        -31.68115742348633,
        -31.6956127200013,
        -31.70968919876564,
        -31.723966657236943,
        -31.738450917699303,
        -31.752531346223417,
        -31.76681286806482,
        -31.78066699393574,
        -31.79471575628544,
        -31.808964702026962,
        -31.823419618626037,
        -31.837415181959273,
        -31.8516094047249,
        -31.865317638578095,
        -31.879216402968908,
        -31.893311069000095,
        -31.907607238144433,
        -31.921380562076607,
        -31.93534624293858,
        -31.949509729798443,
        -31.96311538185422,
        -31.977680606765137,
        -31.990894945961298,
        -32.00507958095325,
        -32.01866348938807,
        -32.03325045791995,
        -32.046397730283985,
        -32.06055873327348,
        -32.074072452440205,
        -32.087771296798365,
        -32.101660408959034,
        -32.11574514884077,
        -32.12913222962323,
        -32.1427009588293,
        -32.156456333897786,
        -32.170403561378635,
        -32.18359885179747,
        -32.19793258979955,
        -32.21149868932627,
        -32.22426273105137,
        -32.23819330458731,
        -32.25171111357468,
        -32.265311200490494,
        -32.27878569954906,
        -32.29223269280026,
        -32.30575576530255,
        -32.31924687705396,
        -32.33259207620299,
        -32.34611778129524,
        -32.359489518261135,
        -32.372813179459605,
        -32.3865491835052
    ]

    return math.exp(logs[i] + (logs[i+1] - logs[i]) * f) * 1000

airDensity = airDensityLogMSIS


def luminousEfficiency(speed):
    if speed < 6200:
        return 0
    elif speed < 20000:
        zeta = (-2.1887e-9 + 4.2903e-13 * speed - 1.2447e-17 * speed**2) * speed**2
    elif speed < 60000:
        zeta = 2.37044e-6 * speed**1.25
    elif speed < 100000:
        zeta = -12.835 + speed * (6.7672e-4 + speed * (-1.163076e-8 + speed * (9.191681e-14 + speed * -2.7465805e-19)))
    else:
        zeta = 1.615 + speed * 1.3725e-5

    return 2 * 7.668e6 * zeta / speed**2
