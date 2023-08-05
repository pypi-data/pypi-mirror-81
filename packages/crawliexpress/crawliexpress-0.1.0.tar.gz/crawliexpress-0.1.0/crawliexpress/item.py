from crawliexpress.exception import CrawliexpressException

import re
import json
import _jsonnet


RUN_PARAMS_RE = re.compile(r"window\.runParams = ({.+?});$", re.MULTILINE | re.DOTALL)


class Item:
    run_params = None
    product_id = None
    owner_member_id = None
    company_id = None

    def from_html(self, html):

        matches = RUN_PARAMS_RE.search(html)
        if matches is None:
            raise CrawliexpressException("could not find runParams")

        self.run_params = run_params = json.loads(
            _jsonnet.evaluate_snippet("snippet", matches.group(1))
        )
        if "data" not in run_params or "feedbackModule" not in run_params["data"]:
            raise CrawliexpressException("unknown runParams structure")

        feedback_module = run_params["data"]["feedbackModule"]

        self.product_id = feedback_module["productId"]
        self.owner_member_id = feedback_module["sellerAdminSeq"]
        self.company_id = feedback_module["companyId"]
