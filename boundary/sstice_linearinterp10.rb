# SST,海氷データをモデル解像度に変換
#
# history:
# sst_HadISST1.F,ice_HadISST1.F mj98用 BCDATA以下にある。(02/08/15)
#   ( + yunix.F tooll.F misc.F gauss.F )
# mkaobnd_with_TaylorCorrection.f90 :
#  This program is based on
#    http://www-pcmdi.llnl.gov/amip/AMIP2EXPDSN/BCS/amip2bcs.html
#  and the Numerical Recipe in Fortran.
#                                       Jul 4, 2003, O. ARAKAWA
# 03/07/23 ver.1 sstice.F F77形式部分   R.Mizuta
# 03/07/23 ver.2 sst_HadISST.Fとice_HadISST.Fを統合   R.Mizuta
# 03/10/07 ver.3 sstice.f90と統合   R.Mizuta
# 06/07/10 sstice_forGSM.rb Rubyに移植、しようとして挫折
# 07/06/07 sstice_interptest.rb バグ修正、コアはtooll.FをRuby化したもの。
# 07/06/07   ver.2 入出力とも北からでも南からでもOK
# 07/06/07 sstice_linearinterp.rb 名前変更
# 07/09/10   ver.2 設定部分を前にもってきた。
# 07/11/16   ver.3 ctlファイルでfile.put_att("yrev",true)としていたバグ修正
# 08/06/26   ver.4 legendre.soを使わないよう変更
# 10/02/10 sstice_linearinterp_core.rb コア部分を分離
# 10/10/08         factor,offsetを設定できるように
# 11/04/17   ver.2 imaxa,jmaxaは自動計算、gaussian可動化のフラグ
# 15/02/10   ver.3 出力ファイル名を変更
# 16/01/14 sstice_linearinterp.rb ver.9 分離を戻し、単独で実行できるように
# 16/04/05   ver.10 sstice_linearinterpの入力引数をファイル名+変数名からGPhysに
#-----------------------------------------------------------------------------#
require "numru/gphys"
include NumRu
include NMath

def lonset(lon_in,lon_out)

  len_in = lon_in.length
  len_out = lon_out.length

  iptlon1 = NArray.int(len_out)
  iptlon2 = NArray.int(len_out)
  wgt = NArray.sfloat(len_out)

#  ic = 0
    wgt_tmp = - (lon_out-lon_in[0]) / (lon_in[0]-lon_in[-1]+360.0)
    inner = ( wgt_tmp >= 0.0 )*( wgt_tmp < 1.0 )
    iptlon1[inner] = -1
    iptlon2[inner] = 0
    wgt[inner] = wgt_tmp[inner]

  for ic in 1..len_in-1
    wgt_tmp = - (lon_out-lon_in[ic]) / (lon_in[ic]-lon_in[ic-1])
    inner = ( wgt_tmp >= 0.0 )*( wgt_tmp < 1.0 )
    iptlon1[inner] = ic-1
    iptlon2[inner] = ic
    wgt[inner] = wgt_tmp[inner]
  end

#  ic in len_in
    wgt_tmp = - (lon_out-lon_in[0]-360.0) / (lon_in[0]-lon_in[-1]+360.0)
    inner = ( wgt_tmp >= 0.0 )*( wgt_tmp < 1.0 )
    iptlon1[inner] = -1
    iptlon2[inner] = 0
    wgt[inner] = wgt_tmp[inner]

  return iptlon1,iptlon2,wgt

end

def latset(lat_in,lat_out)

  inc_in = lat_in[1]-lat_in[0]
  inc_out = lat_out[1]-lat_out[0]

#  raise "lat_in must be from north to south" if inc_in > 0.0
#  raise "lat_out must be from north to south" if inc_out > 0.0

  if( inc_in > 0.0 )
    jflag_in = 1
  else
    jflag_in = -1
  end

  if( inc_out > 0.0 )
    jflag_out = 1
  else
    jflag_out = -1
  end

  lat_in = lat_in[-1..0] if( jflag_in*jflag_out == -1 )

  len_in = lat_in.length
  len_out = lat_out.length

  jptlat1 = NArray.int(len_out)
  jptlat2 = NArray.int(len_out)
  wgt = NArray.sfloat(len_out)

#  ic = 0
    wgt_tmp =   (lat_out-lat_in[0])
    outer = ( wgt_tmp > 0.0 )
    jptlat1[outer] = 0
    jptlat2[outer] = 0
    wgt[outer] = 1.0

  for ic in 1..len_in-1
    wgt_tmp = - (lat_out-lat_in[ic]) / (lat_in[ic]-lat_in[ic-1])
    inner = ( wgt_tmp >= 0.0 )*( wgt_tmp < 1.0 )
    jptlat1[inner] = ic-1
    jptlat2[inner] = ic
    wgt[inner] = wgt_tmp[inner]
  end

#  ic in len_in
    wgt_tmp = - (lat_out-lat_in[-1])
#    outer = ( wgt_tmp < 0.0 ) # bug
    outer = ( wgt_tmp >= 0.0 )
    jptlat1[outer] = -1
    jptlat2[outer] = -1
    wgt[outer] = 1.0

  return jptlat1,jptlat2,wgt,jflag_in,jflag_out

end

def lonint( datain, iptlon1, iptlon2, wgtlon)

  lon_out = iptlon1.length
  lat_out = datain.shape[1]

  dataout = NArrayMiss.sfloat(lon_out,lat_out)
  for i in 0..lon_out-1
    dataout[i,true] = datain[iptlon1[i],true].val*wgtlon[i] + 
                      datain[iptlon2[i],true].val*(1.0-wgtlon[i])
  end

  return dataout
end

def latint( datain, jptlat1, jptlat2, wgtlat,jflag_in,jflag_out)

  lon_out = datain.shape[0]
  lat_out = jptlat1.length

  dataout = NArrayMiss.sfloat(lon_out,lat_out)

  if( jflag_in*jflag_out == 1 )
    for j in 0..lat_out-1
      dataout[true,j] = datain[true,jptlat1[j]]*wgtlat[j] + 
                        datain[true,jptlat2[j]]*(1.0-wgtlat[j])
    end
  else
    for j in 0..lat_out-1
      dataout[true,j] = datain[true,-1-jptlat1[j]]*wgtlat[j] + 
                        datain[true,-1-jptlat2[j]]*(1.0-wgtlat[j])
    end
  end

  return dataout
end

def sstice_linearinterp(
  var_in, grid_out, 
  outfilenamebase,
  yearmin,yearmax,monmax=12,factor=1.0,offset=0.0,
  gaussian_in=false,gaussian_out=false
)

#  p infilename
#  var_in = GPhys::IO.open(infilename,varname)

  lon_in = var_in.coord(0).val
  lat_in = var_in.coord(1).val

#  grid_out = GPhys::IO.open(gridfilename,gridvarname)

  lon_out = grid_out.axis(0).pos.val
  lat_out = grid_out.axis(1).pos.val

  # コントロールファイルの緯度は5ケタしかないので計算し直し
  if gaussian_in
    require "gauss1.rb"
    jmaxa = lat_in.length
    coscolat = Gauss.gauss_lat(jmaxa)

    if lat_in[0] < lat_in[-1]
      lat_in = acos(coscolat)*180.0/PI - 90.0
    else
      lat_in = 90.0 - acos(coscolat)*180.0/PI
    end
  end

  if gaussian_out
    require "gauss1.rb"
    jmaxa = lat_out.length
    coscolat = Gauss.gauss_lat(jmaxa)

    p lat_out[0]
    p lat_out[-1]

    if lat_out[0] < lat_out[-1]
      lat_out = acos(coscolat)*180.0/PI - 90.0
    else
      lat_out = 90.0 - acos(coscolat)*180.0/PI
    end
    p lat_out[0]
    p lat_out[-1]
  end

  iptlon1,iptlon2,wgtlon = lonset(lon_in,lon_out)
  jptlat1,jptlat2,wgtlat,jflag_in,jflag_out = latset(lat_in,lat_out)

  p iptlon1,iptlon2,wgtlon
  p jptlat1,jptlat2,wgtlat,jflag_in,jflag_out

  for year in yearmin..yearmax
  #for year in yearmin_out..yearmax_out

    monmin1 = 1
    monmax1 = 12
    monmax1 = monmax if year == yearmax

    grid = grid_out[false,monmin1-1..monmax1-1].grid_copy

    datemin = Date.new(year,monmin1,10)
#    datemax = Date.new(year,monmax1,10)
    datemax = Date.new(year,monmax1,20)

    grid.axis(-1).pos.val = var_in.axis(-1).cut(datemin..datemax)[0].pos.val

    nary_out = NArrayMiss.sfloat(*grid.shape)
    var_out = GPhys.new(grid,VArray.new(nary_out))

    for mon in monmin1..monmax1
      date = Date.new(year,mon,10)
      a = lonint( var_in.cut(false,date).first2D, iptlon1,iptlon2,wgtlon)
      b = latint(a, jptlat1, jptlat2, wgtlat,jflag_in,jflag_out)
      p b[lon_out.length/2,lat_out.length/2-3..lat_out.length/2+3]
      nary_out[false,mon-1] = b.newdim(-1)
    end

    # factor,offset
    var_out.data.val = var_out.data.val * factor + offset

    # 欠損値の設定
    var_out.data.val = var_out.data.val.set_missing_value(-9.99e33)

    # ファイル書きだし
  #  file = GrADS_Gridded.create("#{outfilenamebase}_#{year}_.ctl",true)
    file = GrADS_Gridded.create("#{outfilenamebase}_#{year}_.ctl",false)
    if( yearmax != yearmin )
#      file.dset = "#{outfilenamebase}_#{year}"
      file.dset = "#{outfilenamebase}_#{year}.dat"
    else
      file.dset = "#{outfilenamebase}"
    end
    file.put_att("big_endian",true)
    file.put_att("undef",-9.99e33)
    GPhys::GrADS_IO.write(file,var_out)
    file.close

  end
end

if $0 == __FILE__

# 出力解像度
  outresol = ARGV[0]

# 出力と同じグリッドを持つファイル(水平が同じで、時間12ヶ月以上),その中の変数
  gridfilename = "#{outresol}_yrev.ctl"
  gridvarname = "dummy"
  grid_out = GPhys::IO.open(gridfilename,gridvarname)

  gaussian_out = true # 出力のグリッドがgaussianかどうか

# 出力期間
  yearmin = ARGV[1].to_i
  yearmax = ARGV[2].to_i
  monmax = 12

# 入力ファイル・変数
  infilename = ARGV[3]
  varname = ARGV[4]

  p infilename
  var_in = GPhys::IO.open(infilename,varname)

  factor = 1.0
  offset = 0.0
  gaussian_in = false # 入力のグリッドがgaussianかどうか

  outfilenamebase = ARGV[5]

  sstice_linearinterp(
    var_in, grid_out, 
    outfilenamebase,
    yearmin,yearmax,
    monmax,
    factor,offset,
    gaussian_in,gaussian_out
  )

end

