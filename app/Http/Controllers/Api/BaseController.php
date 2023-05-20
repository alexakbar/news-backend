<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class BaseController extends Controller
{
    /**
     * create success response
     * 
     */
    public function sendResponse($result, $message, $code = 200)
    {
        $response = [
            'success' => true,
            'data' => $result,
            'message' => $message,
        ];
        
        return response()->json($response, $code);
    }

    /**
     * create error response
     * 
     */

    public function sendError($error, $dataMessage = [], $code = 400)
    {
        $response = [
            'success' => false,
            'message' => $error,
        ];

        if(!empty($dataMessage)){
            $response['data'] = $dataMessage;
        }

        return response()->json($response, $code);
    }
}
