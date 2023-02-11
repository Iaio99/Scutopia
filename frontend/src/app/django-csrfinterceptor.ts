import { HttpInterceptor, HttpXsrfTokenExtractor, HttpRequest, HttpHandler, HttpEvent } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";


@Injectable()
export class DjangoCSRFInterceptor implements HttpInterceptor {
    constructor(private tokenExtractor: HttpXsrfTokenExtractor) {}

    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        const cookieheaderName = 'X-XSRF-TOKEN';
        let csrfToken = this.tokenExtractor.getToken() as string;

        if (csrfToken !== null && !req.headers.has(cookieheaderName)) {
            req = req.clone({ headers: req.headers.set(cookieheaderName, csrfToken) });
        }

        req = req.clone({ headers: req.headers.set("Access-Control-Allow-Origin", "*")});
        req = req.clone({ headers: req.headers.set("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")});

        return next.handle(req);
    }
}