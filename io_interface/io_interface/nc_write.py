import os
import numpy as np
import netCDF4
import subprocess

def write_1d(output_file, x, var, varname, xname = 'time', xaxis = 'T', tbgn_name = '0001-01', standard_name = '', var_unit = '', long_name = '', ERR = -9.99e33, nc_format = 'NETCDF4', compress = False):

    nc_out = netCDF4.Dataset(output_file, 'w', format= nc_format)
    if xname == 'time':
        nc_out.createDimension(xname, None)
        x_out = nc_out.createVariable(xname, np.dtype('double').char, (xname, ))
        # time_out.long_name = xname
        x_out.units = 'days since ' + (tbgn_name) + '-01 00:00:00'
        x_out.axis = 'T'
    else:
        x_out = nc_out.createVariable(xname, np.dtype('double').char, (xname))
        nc_out.createDimension(xname, np.shape(var)[0])                
        # x_out.xg_name = xname
        # x_out.units = xunit
        x_out.axis = xaxis


    var_out = nc_out.createVariable(varname, np.dtype('float32').char, (xname), fill_value = ERR)
        
    if (standard_name == '')*(var_unit == '') :
        standard_name, var_unit = variable_names(varname)
                
    var_out.standard_name = standard_name    
    var_out.units = var_unit

    if long_name == '':
        var_out.long_name = standard_name
    else:
        var_out.long_name = long_name       


    x_out[:] = x
    var_out[:] = var.astype('float32')

    nc_out.close()
    if compress:
        cmpdir = os.path.dirname(__file__)
        subprocess.run(cmpdir+'/nccomp.sh ' + output_file, shell = True)


def write_woa1x1_3d(output_file, time, lon, lat, var, varname, tbgn_name = '0001-01', standard_name = '', var_unit = '', ERR = -9.99e33, nc_format = 'NETCDF4', compress = False):

    nc_out = netCDF4.Dataset(output_file, 'w', format= nc_format)
    nc_out.createDimension('lon', np.shape(var)[2])                
    nc_out.createDimension('lat', np.shape(var)[1])     
    nc_out.createDimension('time', None) 
    
    lon_out = nc_out.createVariable('lon', np.dtype('double').char, ('lon'))
    # lon_out.long_name = 'longitude'
    # lon_out.units = 'degrees_east'
    lon_out.axis = 'X'
    
    lat_out = nc_out.createVariable('lat', np.dtype('double').char, ('lat'))
    # lat_out.long_name = 'latitude'
    # lat_out.units = 'degrees_north'
    lat_out.axis = 'Y'
    
    
    time_out = nc_out.createVariable('time', np.dtype('double').char, ('time', ))
    # time_out.long_name = 'time'
    time_out.units = 'days since ' + (tbgn_name) + '-01 00:00:00'
    time_out.axis = 'T'
    # time_out.calendar = 'proleptic_gregorian'
    
    # var_out = nc_out.createVariable(varname, np.dtype('float32').char, ('time', 'lat', 'lon'), fill_value = np.array(ERR, dtype = 'float32'))

    var_out = nc_out.createVariable(varname, np.dtype('float32').char, ('time', 'lat', 'lon'), fill_value = ERR)

    if (standard_name == '')*(var_unit == '') :
        standard_name, var_unit = variable_names(varname)
        
    var_out.long_name = standard_name
    var_out.units = var_unit


    lon_out[:] = lon
    lat_out[:] = lat
    time_out[:] = time
    var_out[:,:,:] = var.astype('float32')

    nc_out.close()

    if compress:
        cmpdir = os.path.dirname(__file__)
        subprocess.run(cmpdir+'/nccomp.sh ' + ofbase+str(year)+'.nc', shell = True)

    

def write_woa1x1_4d(output_file, time, depth, lon, lat, var, varname, tbgn_name = '0001-01', standard_name = '', var_unit = '', ERR = -9.99e33, nc_format = 'NETCDF4', compress = False):

    nc_out = netCDF4.Dataset(output_file, 'w', format= nc_format)
    nc_out.createDimension('lon', np.shape(var)[3])                
    nc_out.createDimension('lat', np.shape(var)[2])     
    nc_out.createDimension('depth', np.shape(var)[1])     
    nc_out.createDimension('time', None) 
    
    lon_out = nc_out.createVariable('lon', np.dtype('double').char, ('lon'))
    # lon_out.long_name = 'longitude'
    # lon_out.units = 'degrees_east'
    lon_out.axis = 'X'
    
    lat_out = nc_out.createVariable('lat', np.dtype('double').char, ('lat'))
    # lat_out.long_name = 'latitude'
    # lat_out.units = 'degrees_north'
    lat_out.axis = 'Y'
    
    depth_out = nc_out.createVariable('depth', np.dtype('double').char, ('depth'))
    # depth_out.long_name = 'depth'
    # depth_out.units = 'm'
    depth_out.axis = 'Z'
    
    time_out = nc_out.createVariable('time', np.dtype('double').char, ('time', ))
    # time_out.long_name = 'time'
    time_out.units = 'days since ' + (tbgn_name) + '-01 00:00:00'
    time_out.axis = 'T'
    # time_out.calendar = 'proleptic_gregorian'
    
    # var_out = nc_out.createVariable(varname, np.dtype('float32').char, ('time', 'depth', 'lat', 'lon'), fill_value = np.array(ERR, dtype = 'float32'))

    var_out = nc_out.createVariable(varname, np.dtype('float32').char, ('time', 'depth', 'lat', 'lon'), fill_value = ERR)

    if (standard_name == '')*(var_unit == '') :
        standard_name, var_unit = variable_names(varname)
        
    var_out.long_name = standard_name
    var_out.units = var_unit


    lon_out[:] = lon
    lat_out[:] = lat
    depth_out[:] = depth
    time_out[:] = time
    var_out[:,:,:,:] = var.astype('float32')
    nc_out.close()

    if compress:
        cmpdir = os.path.dirname(__file__)
        subprocess.run(cmpdir+'/nccomp.sh ' + output_file, shell = True)
    



def write_woa1x1_3d_MVS(output_file, time, lon, lat, vrbs, varnames, tbgn_name = '0001-01', standard_names = [''], var_units = [''], ERR = -9.99e33, nc_format = 'NETCDF4', compress = False):

    nc_out = netCDF4.Dataset(output_file, 'w', format= nc_format)
    nc_out.createDimension('lon', np.size(lon))                
    nc_out.createDimension('lat', np.size(lat))     
    nc_out.createDimension('time', None) 
    
    lon_out = nc_out.createVariable('lon', np.dtype('double').char, ('lon'))
    # lon_out.long_name = 'longitude'
    # lon_out.units = 'degrees_east'
    lon_out.axis = 'X'
    lon_out[:] = lon
    
    lat_out = nc_out.createVariable('lat', np.dtype('double').char, ('lat'))
    # lat_out.long_name = 'latitude'
    # lat_out.units = 'degrees_north'
    lat_out.axis = 'Y'
    lat_out[:] = lat
     
    time_out = nc_out.createVariable('time', np.dtype('double').char, ('time', ))
    # time_out.long_name = 'time'
    time_out.units = 'days since ' + (tbgn_name) + '-01 00:00:00'
    time_out.axis = 'T'
    # time_out.calendar = 'proleptic_gregorian'
    time_out[:] = time
    

    
    if np.size(standard_names) == 1:
        standard_names = np.tile(standard_names, np.size(varnames))
    if np.size(var_units) == 1:
        var_units = np.tile(var_units, np.size(varnames))
    
    for n in range(np.size(varnames)):
        varname = varnames[n]
        var = vrbs[n]
        standard_name = standard_names[n]
        var_unit = var_units[n]

        # var_out = nc_out.createVariable(varname, np.dtype('float32').char, ('time', 'depth', 'lat', 'lon'), fill_value = ERR)
        var_out = nc_out.createVariable(varname, np.dtype('float32').char, ('time', 'lat', 'lon'), fill_value = ERR)
    
        if (standard_name == '')*(var_unit == '') :
            standard_name, var_unit = variable_names(varname)
        
        var_out.long_name = standard_name
        var_out.units = var_unit
        var_out[:,:,:] = var.astype('float32')        

    nc_out.close()

    if compress:
        cmpdir = os.path.dirname(__file__)
        subprocess.run(cmpdir+'/nccomp.sh ' + output_file, shell = True)
    
def write_woa1x1_4d_MVS(output_file, time, depth, lon, lat, vrbs, varnames, tbgn_name = '0001-01', standard_names = [''], var_units = [''], ERR = -9.99e33, nc_format = 'NETCDF4', compress = False):

    nc_out = netCDF4.Dataset(output_file, 'w', format= nc_format)
    nc_out.createDimension('lon', np.size(lon))                
    nc_out.createDimension('lat', np.size(lat))     
    nc_out.createDimension('depth', np.size(depth))     
    nc_out.createDimension('time', None) 
    
    lon_out = nc_out.createVariable('lon', np.dtype('double').char, ('lon'))
    # lon_out.long_name = 'longitude'
    # lon_out.units = 'degrees_east'
    lon_out.axis = 'X'
    lon_out[:] = lon
    
    lat_out = nc_out.createVariable('lat', np.dtype('double').char, ('lat'))
    # lat_out.long_name = 'latitude'
    # lat_out.units = 'degrees_north'
    lat_out.axis = 'Y'
    lat_out[:] = lat
    
    depth_out = nc_out.createVariable('depth', np.dtype('double').char, ('depth'))
    # depth_out.long_name = 'depth'
    # depth_out.units = 'm'
    depth_out.axis = 'Z'
    depth_out[:] = depth    
    time_out = nc_out.createVariable('time', np.dtype('double').char, ('time', ))
    # time_out.long_name = 'time'
    time_out.units = 'days since ' + (tbgn_name) + '-01 00:00:00'
    time_out.axis = 'T'
    # time_out.calendar = 'proleptic_gregorian'
    time_out[:] = time
    

    if np.size(standard_names) == 1:
        standard_names = np.tile(standard_names, np.size(varnames))
    if np.size(var_units) == 1:
        var_units = np.tile(var_units, np.size(varnames))
    
    for n in range(np.size(varnames)):
        varname = varnames[n]
        var = vrbs[n]
        standard_name = standard_names[n]
        var_unit = var_units[n]

        # var_out = nc_out.createVariable(varname, np.dtype('float32').char, ('time', 'depth', 'lat', 'lon'), fill_value = np.array(ERR, dtype = 'float32'))
        var_out = nc_out.createVariable(varname, np.dtype('float32').char, ('time', 'depth', 'lat', 'lon'), fill_value = ERR)

        if (standard_name == '')*(var_unit == '') :
            standard_name, var_unit = variable_names(varname)
        
        var_out.long_name = standard_name
        var_out.units = var_unit
        var_out[:,:,:,:] = var.astype('float32')

    nc_out.close()

    if compress:
        cmpdir = os.path.dirname(__file__)
        subprocess.run(cmpdir+'/nccomp.sh ' + output_file, shell = True)
    



def variable_names(varname):
    standard_name = ''
    var_unit = ''
    if(varname == 'thetao'):
        standard_name = 'sea_water_potential_temprature'
        var_unit = 'degC'
    if(varname == 'tos'):
        standard_name = 'sea_surface_temprature'
        var_unit = 'degC'
    if(varname == 'so'):
        standard_name = 'sea_water_salinity'
        var_unit = '1e-3'
    if(varname == 'siconc'):
        standard_name = 'sea_ice_area_fraction'
        var_unit = ''
    if(varname == 'area'):
        standard_name = 'area'
        var_unit = 'm^2'        
    if 'siarea' in varname:
        standard_name = 'sea_ice_area'
        var_unit = '1e6 km2'
    
            
    return standard_name, var_unit
        
    


    
    
