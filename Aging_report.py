from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from bimal_admin.utils.jwt_authentication import CustomJWTAuthentication
from bimal_admin.utils.pagination import raw_paginations

class AgingReport(APIView): 
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        success = False
        data = None
        message = "Aging reports retrieval failed."
        response_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        
        try:
            Variant = request.data.get("Variant")
            
            print(f"Variant received: {Variant}")
            
            
            
            

            raw_query = f"""
                SELECT    
                       dms_retail.variant_desc AS Variant_Description,
                       dms_retail.clr_desc,
                       dms_retail.vin,
                       dms_retail.mul_inv_dt AS Invoice_Date,
                       dms_stock.ageing
                FROM
                    dms_retail
                         
                LEFT JOIN   
                    dms_stock
                ON
                    dms_retail.vin = dms_stock.vin_number    
                       
                       
                                             
                       
            """     
            # Adding filters dynamically
            where_conditions = "WHERE 1=1"
            
            if Variant:
                where_conditions += f" AND dms_retail.variant_desc = '{Variant}'"
                    
            raw_query += where_conditions
            
            print(f"Final Query: {raw_query}")
            
            
            search_columns = ["dms_retail.vin", "dms_retail.mul_inv_dt"]
            order_column_name = "dms_retail.mul_inv_dt"
            is_loading_all = False
            group_by = ""  # Not required unless aggregation needed

            records, success = raw_paginations(
                request,
                raw_query,
                search_columns,
                order_column_name,
                is_loading_all,
                "",
                group_by,
            )

            if success:
                data = records
                message = "Aging reports retrieved successfully."
                response_code = status.HTTP_200_OK
            else:
                message = "No records found for the given filters."
                response_code = status.HTTP_404_NOT_FOUND
        except Exception as e:
            message = f"An error occurred: {str(e)}"

        return Response(
            {"success": success, "data": data, "message": message}, status=response_code
        )
        

